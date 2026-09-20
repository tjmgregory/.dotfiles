#!/usr/bin/env python3
"""Teleport: explicit, recoverable session transfers over existing SSH access."""
import argparse
import contextlib
import hashlib
import fcntl
import json
import os
from pathlib import Path
import queue
import re
import shlex
import shutil
import sqlite3
import subprocess
import sys
import tarfile
import tempfile
import threading
import time
import uuid
import tomllib

VERSION = '0.1.0'
SELF = Path(__file__).resolve()
ROOT = Path.home() / '.local/share/teleport'
REMOTE_SCRIPT = '.dotfiles/agents/skills/teleport/scripts/teleport.py'


def run(args, cwd=None, data=None, timeout=120, check=True):
    p = subprocess.run([str(x) for x in args], cwd=cwd, input=data,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    if check and p.returncode:
        raise RuntimeError(f'{args[0]} failed ({p.returncode}): {p.stderr.decode(errors="replace")[-1500:]}')
    return p


def out(args, **kw):
    return run(args, **kw).stdout.decode().strip()


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    tmp = path.with_suffix('.pending')
    tmp.write_text(json.dumps(value, indent=2) + '\n')
    tmp.chmod(0o600)
    tmp.replace(path)


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def response_digest(path):
    def normalized(value):
        # Native Codex deserialization omits optional null fields (notably
        # reasoning.content). This is the only normalization we permit.
        if isinstance(value, dict):
            return {k: normalized(v) for k, v in value.items() if v is not None}
        if isinstance(value, list):
            return [normalized(v) for v in value]
        return value
    h = hashlib.sha256()
    count = 0
    for line in Path(path).open():
        d = json.loads(line)
        if d.get('type') == 'response_item':
            h.update(json.dumps(normalized(d['payload']), sort_keys=True, separators=(',', ':')).encode())
            count += 1
    return count, h.hexdigest()


def readable_history(source, dest, kind):
    with Path(dest).open('w') as output:
        for line in Path(source).open():
            d = json.loads(line)
            msg = d.get('payload', {}) if kind == 'codex' else d.get('message', {})
            if kind == 'codex' and d.get('type') != 'response_item':
                continue
            role = msg.get('role')
            if role not in ('user', 'assistant'):
                continue
            content = msg.get('content', [])
            if isinstance(content, str):
                texts = [content]
            else:
                texts = [x.get('text', '') for x in content if x.get('type') in ('text', 'input_text', 'output_text')]
            if any(texts):
                output.write('\n## ' + role + '\n\n' + '\n'.join(texts) + '\n')


class RPC:
    def __init__(self):
        self.log = tempfile.NamedTemporaryFile(prefix='teleport-rpc-', suffix='.log', dir='/tmp', mode='w', delete=False)
        self.p = subprocess.Popen(['codex', 'app-server', '--stdio'], stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, stderr=self.log, text=True)
        self.q = queue.Queue()
        self.seq = 0
        def reader():
            for line in self.p.stdout:
                try:
                    self.q.put(json.loads(line))
                except ValueError:
                    pass
            self.q.put(None)
        threading.Thread(target=reader, daemon=True).start()
        self.call('initialize', {'clientInfo': {'name': 'teleport', 'version': VERSION},
                                'capabilities': {'experimentalApi': True}})

    def call(self, method, params, timeout=180):
        self.seq += 1
        self.p.stdin.write(json.dumps({'id': self.seq, 'method': method, 'params': params}) + '\n')
        self.p.stdin.flush()
        end = time.monotonic() + timeout
        while True:
            d = self.q.get(timeout=max(0.1, end - time.monotonic()))
            if d is None:
                raise RuntimeError('Codex app server exited')
            if d.get('id') == self.seq:
                if 'error' in d:
                    raise RuntimeError(str(d['error']))
                return d.get('result', {})

    def close(self):
        self.p.stdin.close()
        try:
            self.p.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.p.terminate()
            self.p.wait(timeout=10)
        self.log.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def herdr(*args):
    return json.loads(out(['herdr', *args]))['result']


def live_agents():
    agents = herdr('agent', 'list')['agents']
    for agent in agents:
        if not (agent.get('agent_session') or {}).get('value'):
            info = herdr('pane', 'process-info', '--pane', agent['pane_id'])['process_info']
            for proc in info['foreground_processes']:
                args = proc.get('argv', [])
                for flag in ('resume', '--resume', '--session-id'):
                    if flag in args and len(args) > args.index(flag) + 1:
                        sid = args[args.index(flag) + 1]
                        try:
                            uuid.UUID(sid)
                        except ValueError:
                            continue
                        agent['agent_session'] = {'value': sid, 'source': 'process-argv'}
    return agents


def writer_active(sid):
    path = Path.home() / '.codex/thread-writer-locks' / (sid + '.lock')
    if not path.exists():
        return False
    with path.open('r') as f:
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return True
        fcntl.flock(f, fcntl.LOCK_UN)
    return False


def codex_meta(sid):
    path = Path.home() / '.codex/state_5.sqlite'
    with sqlite3.connect(path.as_uri() + '?mode=ro', uri=True) as c:
        row = c.execute('select id,rollout_path,cwd,name,history_mode,cli_version from threads where id=?', (sid,)).fetchone()
    if row is None:
        raise RuntimeError('Exact Codex session ID is not indexed locally')
    return dict(zip(('id', 'path', 'cwd', 'name', 'historyMode', 'cliVersion'), row))


def sessions(kind, query_text=''):
    rows = []
    if kind == 'codex':
        db = Path.home() / '.codex/state_5.sqlite'
        with sqlite3.connect(db.as_uri() + '?mode=ro', uri=True) as c:
            for sid, name, title, cwd, updated in c.execute(
                    'select id,name,title,cwd,updated_at from threads where archived=0 order by updated_at desc'):
                label = name or title[:100]
                if query_text.lower() in (label + ' ' + title).lower():
                    rows.append({'id': sid, 'name': label, 'cwd': cwd, 'updated': updated})
    else:
        for p in (Path.home() / '.claude/projects').glob('*/*.jsonl'):
            if query_text and query_text.lower() not in p.stem.lower():
                continue
            rows.append({'id': p.stem, 'path': str(p), 'updated': p.stat().st_mtime})
        rows.sort(key=lambda r: r['updated'], reverse=True)
    return rows[:50]


def secret_path(p):
    parts = Path(p).parts
    return any(x in {'.git', '.ssh', '.aws', '.gnupg'}
               or x == '.env' or x.startswith('.env.') and x not in {'.env.example', '.env.template', '.env.tpl', '.env.sample'}
               or x.endswith(('.pem', '.key', '.p12')) for x in parts)


def add_file(tf, path, name):
    if Path(path).is_symlink():
        raise RuntimeError(f'Symlink requires an explicit portable replacement: {path}')
    tf.add(path, arcname=name, recursive=False)


def git(cwd, *args, **kw):
    return run(['git', '-C', str(cwd), *args], **kw)


def gt(cwd, *args):
    return git(cwd, *args).stdout.decode().strip()


def work_fingerprint(repo):
    h = hashlib.sha256()
    for args in [('rev-parse', 'HEAD'), ('diff', '--cached', '--binary', '--full-index'),
                 ('diff', '--binary', '--full-index'), ('status', '--porcelain=v1', '-z')]:
        h.update(git(repo, *args).stdout)
    for rel in git(repo, 'ls-files', '--others', '--exclude-standard', '-z').stdout.decode().split('\0'):
        if rel and not secret_path(rel) and (repo / rel).is_file() and not (repo / rel).is_symlink():
            h.update(rel.encode())
            h.update(sha(repo / rel).encode())
    return h.hexdigest()


def workspace_export(cwd, stage, selected, include=()):
    cwd = Path(cwd).resolve()
    root_result = git(cwd, 'rev-parse', '--show-toplevel', check=False)
    if root_result.returncode == 0:
        root = Path(root_result.stdout.decode().strip())
        repos = [root]
        base = root
    else:
        base = cwd
        repos = [p for p in sorted(cwd.iterdir()) if p.is_dir() and (p / '.git').exists()]
        if selected:
            wanted = set(selected)
            repos = [p for p in repos if p.name in wanted]
            if {p.name for p in repos} != wanted:
                raise RuntimeError('A requested repository was not found directly under cwd')
        elif len(repos) > 8:
            raise RuntimeError(f'{len(repos)} repositories under cwd; select relevant ones with repeated --repo NAME')
    meta = {'base': str(base), 'cwd_relative': str(cwd.relative_to(base)), 'repos': [], 'excluded': []}
    for i, repo in enumerate(repos):
        rd = stage / 'work' / str(i)
        rd.mkdir(parents=True)
        head = gt(repo, 'rev-parse', 'HEAD')
        branch = gt(repo, 'rev-parse', '--abbrev-ref', 'HEAD')
        if gt(repo, 'ls-files', '--unmerged'):
            raise RuntimeError(f'Unresolved conflicts in {repo}')
        if (repo / '.gitmodules').exists():
            raise RuntimeError(f'Submodule workspace needs explicit handling: {repo}')
        tracked = git(repo, 'ls-files', '-z').stdout.decode().split('\0')
        sensitive = [p for p in tracked if p and secret_path(p)]
        if sensitive:
            raise RuntimeError(f'Tracked credential paths in {repo}: {sensitive[:5]}')
        fingerprint = work_fingerprint(repo)
        git(repo, 'bundle', 'create', str(rd / 'commits.bundle'), 'HEAD', timeout=600)
        (rd / 'index.patch').write_bytes(git(repo, 'diff', '--cached', '--binary', '--full-index').stdout)
        (rd / 'work.patch').write_bytes(git(repo, 'diff', '--binary', '--full-index').stdout)
        untracked = git(repo, 'ls-files', '--others', '--exclude-standard', '-z').stdout.decode().split('\0')
        with tarfile.open(rd / 'untracked.tar', 'w') as tf:
            for rel in untracked:
                if not rel:
                    continue
                if secret_path(rel):
                    meta['excluded'].append(str(repo / rel))
                else:
                    add_file(tf, repo / rel, rel)
        remote = git(repo, 'remote', 'get-url', 'origin', check=False).stdout.decode().strip()
        if re.search(r'https?://[^/]*@', remote):
            remote = ''
        meta['repos'].append({'slot': str(i), 'relative': str(repo.relative_to(base)),
                              'head': head, 'branch': branch, 'origin': remote})
        if fingerprint != work_fingerprint(repo):
            raise RuntimeError(f'Workspace changed during snapshot: {repo}; no destination was started')
    # Loose files are intentionally explicit; never recurse across a home or umbrella directory.
    with tarfile.open(stage / 'loose.tar', 'w') as tf:
        if base == cwd and not (base / '.git').exists():
            for p in cwd.iterdir():
                if p.is_file() and p.name in {'AGENTS.md', 'CLAUDE.md', 'skills-lock.json'}:
                    # Shared instruction symlinks become ordinary portable files.
                    add_file(tf, p.resolve(), p.name)
        for rel in include:
            p = Path(rel)
            if p.is_absolute() or '..' in p.parts or secret_path(p):
                raise RuntimeError(f'Unsafe or credential include path: {rel}')
            target = cwd / p
            if not target.is_file():
                raise RuntimeError(f'--include requires an existing file: {rel}')
            add_file(tf, target, str(target.relative_to(base)))
    return meta


def extract_safe(archive, dest):
    dest = Path(dest)
    with tarfile.open(archive) as tf:
        for m in tf.getmembers():
            p = Path(m.name)
            if p.is_absolute() or '..' in p.parts or not (m.isfile() or m.isdir()):
                raise RuntimeError(f'Unsafe archive member: {m.name}')
            target = dest / p
            if any(x.is_symlink() for x in [target, *target.parents]):
                raise RuntimeError('Refusing extraction through symlink')
        tf.extractall(dest)


def workspace_restore(stage, meta, run_id):
    base = Path.home() / 'teleport-workspaces' / run_id
    if base.exists():
        raise RuntimeError(f'Destination workspace already exists: {base}')
    base.mkdir(parents=True, mode=0o700)
    for repo in meta['repos']:
        rd = stage / 'work' / repo['slot']
        dst = base / repo['relative']
        git(base, 'clone', '--no-checkout', str(rd / 'commits.bundle'), str(dst), timeout=600)
        git(dst, 'checkout', '--detach', repo['head'])
        if repo['branch'] != 'HEAD':
            git(dst, 'checkout', '-b', repo['branch'])
        if repo['origin']:
            git(dst, 'remote', 'set-url', 'origin', repo['origin'])
        else:
            git(dst, 'remote', 'remove', 'origin')
        for name, flags in [('index.patch', ['--index']), ('work.patch', [])]:
            p = rd / name
            if p.stat().st_size:
                git(dst, 'apply', '--check', *flags, str(p))
                git(dst, 'apply', *flags, str(p))
        extract_safe(rd / 'untracked.tar', dst)
        if gt(dst, 'rev-parse', 'HEAD') != repo['head']:
            raise RuntimeError('Restored Git head differs')
        for name, args in [('index.patch', ['--cached']), ('work.patch', [])]:
            if git(dst, 'diff', *args, '--binary', '--full-index').stdout != (rd / name).read_bytes():
                raise RuntimeError(f'Restored {name} differs')
    extract_safe(stage / 'loose.tar', base)
    cwd = base / meta['cwd_relative']
    cwd.mkdir(parents=True, exist_ok=True)
    return cwd


def resolve_source(kind, sid, pane=None):
    agents = live_agents()
    if pane:
        matches = [a for a in agents if a['pane_id'] == pane]
        if len(matches) != 1:
            raise RuntimeError('Source pane does not contain an agent')
        agent = matches[0]
        if agent['agent'] != kind:
            raise RuntimeError('Source pane agent kind mismatch')
        actual = (agent.get('agent_session') or {}).get('value')
        if sid and sid != actual:
            raise RuntimeError('Source pane session changed')
        sid = actual
    if not sid:
        raise RuntimeError('Pass --session ID or --pane ID; newest-session guessing is disabled')
    matches = [a for a in agents if (a.get('agent_session') or {}).get('value') == sid]
    if len(matches) > 1:
        raise RuntimeError('Multiple live hosts own this session')
    if matches:
        a = matches[0]
        if a['agent_status'] not in ('idle', 'done'):
            raise RuntimeError('Source must finish its turn before teleporting')
        # Exit only this verified idle agent; keep its pane and all workspace processes.
        if kind == 'claude':
            herdr('agent', 'prompt', a['pane_id'], '/exit')
        else:
            herdr('agent', 'send-keys', a['pane_id'], 'ctrl+d')
        end = time.monotonic() + 15
        while time.monotonic() < end:
            if not any((x.get('agent_session') or {}).get('value') == sid for x in live_agents()):
                break
            time.sleep(.25)
        else:
            raise RuntimeError('Source did not exit; no snapshot was taken')
    if kind == 'codex' and writer_active(sid):
        raise RuntimeError('Codex session still has an active writer outside the selected Herdr pane')
    return sid


def export_session(a):
    kind, sid = a['kind'], resolve_source(a['kind'], a.get('session'), a.get('pane'))
    run_id = a['run_id']
    stage = ROOT / 'runs' / run_id / 'export'
    stage.mkdir(parents=True, mode=0o700)
    if kind == 'codex':
        meta = codex_meta(sid)
        src = Path(meta['path'])
        cwd = meta['cwd']
    else:
        paths = list((Path.home() / '.claude/projects').glob(f'*/{sid}.jsonl'))
        if len(paths) != 1:
            raise RuntimeError('Claude session ID must resolve to exactly one transcript')
        src = paths[0]
        cwd = None
        for line in src.open():
            d = json.loads(line)
            cwd = d.get('cwd', cwd)
        if not cwd:
            raise RuntimeError('Claude transcript has no cwd')
        meta = {'id': sid, 'cwd': cwd, 'name': sid}
    before = src.stat()
    shutil.copyfile(src, stage / 'transcript.jsonl')
    after = src.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise RuntimeError('Source transcript changed during snapshot')
    # A paginated rollout retains raw response items. Native fork reconstructs its own indexes.
    raw_count = 0
    for line in (stage / 'transcript.jsonl').open():
        record = json.loads(line)
        if record.get('type') == 'response_item':
            raw_count += 1
    if kind == 'codex' and raw_count == 0:
        raise RuntimeError('Rollout has no response items; cannot prove portable history')
    work = workspace_export(cwd, stage, a.get('repos', []), a.get('include', []))
    manifest = {'version': VERSION, 'run_id': run_id, 'kind': kind, 'source_id': sid,
                'source': meta, 'workspace': work, 'raw_response_items': raw_count,
                'created': time.time(), 'source_version': out([kind, '--version'])}
    manifest['response_digest'] = response_digest(stage / 'transcript.jsonl')[1] if kind == 'codex' else None
    readable_history(stage / 'transcript.jsonl', stage / 'conversation.md', kind)
    config = Path.home() / '.codex/config.toml'
    if kind == 'codex' and config.exists():
        projects = tomllib.loads(config.read_text()).get('projects', {})
        manifest['trusted_workspace'] = projects.get(cwd, {}).get('trust_level') == 'trusted'
    manifest['checksums'] = {str(p.relative_to(stage)): sha(p) for p in stage.rglob('*') if p.is_file()}
    save(stage / 'manifest.json', manifest)
    archive = stage.parent / 'bundle.tar'
    with tarfile.open(archive, 'w') as tf:
        for p in stage.rglob('*'):
            if p.is_file():
                add_file(tf, p, str(p.relative_to(stage)))
    result = {'archive': str(archive), 'sha256': sha(archive), 'manifest': manifest}
    save(stage.parent / 'export.json', result)
    return result


def import_session(a):
    run_id = a['run_id']
    record = ROOT / 'runs' / run_id / 'import.json'
    if record.exists():
        return json.loads(record.read_text())
    archive = Path(a['archive'])
    if sha(archive) != a['sha256']:
        raise RuntimeError('Archive checksum mismatch')
    stage = ROOT / 'runs' / run_id / 'import'
    if stage.exists():
        raise RuntimeError('Incomplete prior import; inspect before retrying')
    stage.mkdir(parents=True, mode=0o700)
    extract_safe(archive, stage)
    m = json.loads((stage / 'manifest.json').read_text())
    if m['kind'] == 'codex' and (not a.get('target_kind') or a['target_kind'] == 'codex'):
        if m['source_version'] != 'codex-cli 0.154.0' or out(['codex', '--version']) != m['source_version']:
            raise RuntimeError('Native Codex transfer is validated on 0.154.0 on both hosts; validate the adapter before using another version')
    for rel, digest in m['checksums'].items():
        if Path(rel).is_absolute() or '..' in Path(rel).parts:
            raise RuntimeError('Unsafe manifest path')
        if sha(stage / rel) != digest:
            raise RuntimeError(f'Bundle member checksum mismatch: {rel}')
    cwd = workspace_restore(stage, m['workspace'], run_id)
    target = a.get('target_kind') or m['kind']
    handover = cwd / 'TELEPORT-HANDOVER.md'
    handover.write_text(f'# Teleport handover\n\nSource: {m["kind"]} {m["source_id"]}\n'
                        f'Previous workspace: {m["workspace"]["base"]}\n'
                        f'Current workspace: {cwd}\n'
                        f'Full source transcript: {stage / "transcript.jsonl"}\n\n'
                        f'Readable conversation: {stage / "conversation.md"}\n\n'
                        'Use current workspace paths when earlier messages reference the old workspace. '
                        'Dependencies, ignored files, credentials and running processes are not transferred. '
                        'Recheck service health and deployment state before acting; old observations may be stale.\n')
    if target == m['kind'] == 'codex':
        # Codex 0.154 discovers paginated source histories only in its sessions tree,
        # even when thread/fork receives an explicit path. Give the import seed its
        # own ID so a returning transfer cannot collide with an existing local chat.
        seed_id = str(uuid.uuid4())
        seed = (Path.home() / '.codex/sessions' / time.strftime('%Y/%m/%d') /
                ('rollout-' + time.strftime('%Y-%m-%dT%H-%M-%S') + '-' + seed_id + '.jsonl'))
        seed.parent.mkdir(parents=True, exist_ok=True)
        with seed.open('x') as f:
            for line in (stage / 'transcript.jsonl').open():
                d = json.loads(line)
                if d.get('type') == 'session_meta':
                    d['payload']['id'] = seed_id
                    d['payload']['session_id'] = seed_id
                    d['payload']['cwd'] = str(cwd)
                    # The copied rollout has no destination projection database.
                    # Ask Codex to read its raw events as a legacy import and let
                    # native migration rebuild the destination's paginated indexes.
                    d['payload']['history_mode'] = 'legacy'
                f.write(json.dumps(d) + '\n')
        with RPC() as rpc:
            t = rpc.call('thread/fork', {'threadId': seed_id, 'path': str(seed),
                         'cwd': str(cwd), 'excludeTurns': True, 'deferGoalContinuation': True}, timeout=600)['thread']
            sid = t['id']
            rpc.call('thread/unsubscribe', {'threadId': sid})
            rpc.call('thread/name/set', {'threadId': sid, 'name': (m['source'].get('name') or 'Teleported chat').removesuffix(' · teleport') + ' · teleport'})
        imported = Path(t['path'])
        count, digest = response_digest(imported)
        if count != m['raw_response_items'] or digest != m['response_digest']:
            raise RuntimeError(f'History verification failed: expected {m["raw_response_items"]}, got {count}')
        launch = ['resume', sid, '-C', str(cwd), '-c', 'check_for_update_on_startup=false']
        if m.get('trusted_workspace') or a.get('trust_workspace'):
            launch.extend(['-c', 'projects.' + json.dumps(str(cwd)) + '.trust_level="trusted"'])
    elif target == m['kind'] == 'claude':
        # Install an independent ID, rewriting structural IDs/cwd only, never historical prose.
        sid = str(uuid.uuid4())
        project = re.sub(r'[^A-Za-z0-9]', '-', str(cwd))
        dst = Path.home() / '.claude/projects' / project / (sid + '.jsonl')
        dst.parent.mkdir(parents=True, exist_ok=True)
        with dst.open('x') as f:
            for line in (stage / 'transcript.jsonl').open():
                d = json.loads(line)
                if 'sessionId' in d:
                    d['sessionId'] = sid
                if 'cwd' in d:
                    d['cwd'] = str(cwd)
                f.write(json.dumps(d) + '\n')
        launch = ['--resume', sid]
    else:
        prompt = (f'Continue the transferred task. Read {handover} and its source transcript first. '
                  'Summarize the current objective, decisions and unfinished work before taking action. '
                  'This is a cross-assistant handover, not a native resumed session.')
        if target == 'codex':
            with RPC() as rpc:
                sid = rpc.call('thread/start', {'cwd': str(cwd)})['thread']['id']
                rpc.call('thread/inject_items', {'threadId': sid, 'items': [
                    {'type': 'message', 'role': 'user', 'content': [{'type': 'input_text', 'text': prompt}]}]})
                rpc.call('thread/unsubscribe', {'threadId': sid})
                rpc.call('thread/name/set', {'threadId': sid, 'name': 'Handover from ' + m['kind']})
            launch = ['resume', sid, '-C', str(cwd), '-c', 'check_for_update_on_startup=false', prompt]
            if a.get('trust_workspace'):
                launch.extend(['-c', 'projects.' + json.dumps(str(cwd)) + '.trust_level="trusted"'])
        else:
            sid = str(uuid.uuid4())
            launch = ['--session-id', sid, prompt]
    result = {'run_id': run_id, 'kind': target, 'session': sid, 'cwd': str(cwd),
              'launch_args': launch, 'handover': str(handover), 'excluded': m['workspace']['excluded'],
              'status': 'imported', 'source_id': m['source_id'],
              'display_name': (m['source'].get('name') or target + ' teleport')[:64]}
    save(record, result)
    return result


def launch_session(a):
    record = ROOT / 'runs' / a['run_id'] / 'import.json'
    r = json.loads(record.read_text())
    pane = r.get('pane')
    if not pane:
        created = herdr('workspace', 'create', '--cwd', r['cwd'], '--label', r.get('display_name', 'teleport ' + a['run_id'][:8]), '--no-focus')
        pane = created['root_pane']['pane_id']
        r.update(pane=pane, workspace=created['workspace']['workspace_id'], status='starting')
        save(record, r)
        try:
            herdr('agent', 'start', 'tp-' + a['run_id'][:12], '--kind', r['kind'], '--pane', pane,
                  '--timeout', '60000', '--', *r['launch_args'])
        except RuntimeError as e:
            r.update(status='needs_attention', startup_error=str(e))
            save(record, r)
            screen = out(['herdr', 'agent', 'read', pane, '--source', 'detection', '--lines', '40'])
            if '3. Continue without trusting' in screen and '1. Review hooks' in screen:
                # Explicitly decline new hook permissions; never trust hooks for a transfer.
                herdr('agent', 'send-keys', pane, '3', 'enter')
            else:
                raise
    end = time.monotonic() + 20
    actual_id = None
    while time.monotonic() < end:
        actual = next((x for x in live_agents() if x['pane_id'] == pane), {})
        actual_id = (actual.get('agent_session') or {}).get('value')
        writer_ready = r['kind'] != 'codex' or actual_id and writer_active(actual_id)
        screen = out(['herdr', 'agent', 'read', pane, '--source', 'detection', '--lines', '40'])
        if 'Press t to trust all' in screen and 'esc to close' in screen:
            # Dismiss the optional hooks review. This does not approve any hook.
            herdr('agent', 'send-keys', pane, 'esc')
            time.sleep(.5)
            continue
        if any(s in screen for s in ('Do you trust the contents of this directory?',
                                     'Quick safety check: Is this a project', 'Press enter to continue')):
            actual['agent_status'] = 'blocked'
        if actual_id and writer_ready and actual.get('agent_status') in ('idle', 'done'):
            break
        if actual.get('agent_status') == 'blocked':
            break
        time.sleep(.5)
    if (not actual_id or not writer_ready or r['session'] and actual_id != r['session']
            or actual.get('agent_status') not in ('idle', 'done', 'working')):
        r['status'] = 'needs_attention'
        save(record, r)
        raise RuntimeError(f'Destination not verified; inspect Herdr pane {pane}, then retry launch {a["run_id"]}')
    r.update(status='ready', session=actual_id or r['session'])
    r.pop('startup_error', None)
    save(record, r)
    return r


def endpoint(host, action, values):
    req = json.dumps({'action': action, **values}).encode()
    if host == 'local':
        return worker(json.loads(req))
    cmd = 'python3 "$HOME/' + REMOTE_SCRIPT + '" worker'
    p = run(['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=10', host, cmd], data=req, timeout=900)
    return json.loads(p.stdout)


def codex_runtime():
    executable = shutil.which('codex')
    helper = Path(executable).resolve().parent / 'codex-code-mode-host' if executable else None
    if not helper or not helper.is_file():
        return {'ready': False, 'error': 'Bundled codex-code-mode-host is missing'}
    try:
        run([helper, '--help'], timeout=10)
        return {'ready': True, 'helper': str(helper)}
    except (RuntimeError, subprocess.TimeoutExpired) as e:
        return {'ready': False, 'helper': str(helper), 'error': str(e)}


def worker(a):
    action = a['action']
    if action == 'doctor':
        return {'version': VERSION, 'codex': out(['codex', '--version']), 'claude': out(['claude', '--version']),
                'herdr': out(['herdr', '--version']), 'agents': live_agents(), 'home': str(Path.home()),
                'codex_runtime': codex_runtime()}
    if action == 'list':
        return sessions(a['kind'], a.get('query', ''))
    if action == 'export':
        return export_session(a)
    if action == 'import':
        return import_session(a)
    if action == 'launch':
        return launch_session(a)
    if action == 'status':
        folder = ROOT / 'runs' / a['run_id']
        path = folder / 'import.json'
        if not path.exists():
            path = folder / 'transfer.json'
        return json.loads(path.read_text())
    raise RuntimeError('Unknown worker action')


def transfer(a):
    if a.source == a.dest:
        raise RuntimeError('Source and destination must differ')
    run_id = a.run_id or uuid.uuid4().hex
    a.run_id = run_id
    record = ROOT / 'runs' / run_id / 'transfer.json'
    state = {'run_id': run_id, 'source': a.source, 'destination': a.dest, 'status': 'preflight'}
    save(record, state)
    destination = endpoint(a.dest, 'doctor', {})
    if (a.as_kind or a.kind) == 'codex' and not destination['codex_runtime']['ready']:
        raise RuntimeError('Destination Codex tool runtime is unavailable; source was not stopped: '
                           + destination['codex_runtime']['error'])
    if a.wait_idle:
        end = time.monotonic() + 600
        while time.monotonic() < end:
            agents = endpoint(a.source, 'doctor', {})['agents']
            matches = [x for x in agents if x['pane_id'] == a.pane] if a.pane else [
                x for x in agents if (x.get('agent_session') or {}).get('value') == a.session]
            if not matches or matches[0]['agent_status'] in ('idle', 'done'):
                break
            time.sleep(2)
        else:
            raise RuntimeError('Source did not become idle within ten minutes')
    exported = endpoint(a.source, 'export', {'run_id': run_id, 'kind': a.kind, 'session': a.session,
                                            'pane': a.pane, 'repos': a.repo, 'include': a.include})
    state.update(status='exported', source_session=exported['manifest']['source_id'])
    save(record, state)
    local_archive = ROOT / 'runs' / run_id / 'received.tar'
    if a.source == 'local':
        local_archive = Path(exported['archive'])
    else:
        run(['scp', '-q', a.source + ':' + exported['archive'], str(local_archive)], timeout=900)
    if a.dest == 'local':
        target_archive = str(local_archive)
    else:
        target_archive = '/tmp/teleport-' + run_id + '.tar'
        run(['scp', '-q', str(local_archive), a.dest + ':' + target_archive], timeout=900)
    result = endpoint(a.dest, 'import', {'run_id': run_id, 'archive': target_archive,
                      'sha256': exported['sha256'], 'target_kind': a.as_kind,
                      'trust_workspace': a.trust_workspace})
    state.update(status='imported', result=result)
    save(record, state)
    if not a.no_launch:
        result = endpoint(a.dest, 'launch', {'run_id': run_id})
    state.update(status=result['status'], result=result)
    save(record, state)
    return state


def main():
    os.umask(0o077)
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('worker')
    for verb in ['doctor', 'list', 'status', 'launch']:
        x = sub.add_parser(verb)
        x.add_argument('--host', default='local')
        if verb == 'list':
            x.add_argument('--kind', choices=['codex', 'claude'], default='codex')
            x.add_argument('--query', default='')
        if verb in ['status', 'launch']:
            x.add_argument('run_id')
    x = sub.add_parser('move')
    x.add_argument('--from', dest='source', default='local')
    x.add_argument('--to', dest='dest', required=True)
    x.add_argument('--kind', choices=['codex', 'claude'], required=True)
    x.add_argument('--session')
    x.add_argument('--pane')
    x.add_argument('--repo', action='append', default=[])
    x.add_argument('--include', action='append', default=[], help='Explicit extra file relative to source cwd; repeat as needed')
    x.add_argument('--as', dest='as_kind', choices=['codex', 'claude'])
    x.add_argument('--no-launch', action='store_true')
    x.add_argument('--trust-workspace', action='store_true', help='Trust the transferred workspace when its contents are already approved')
    x.add_argument('--detach', action='store_true', help='Wait for this conversation to finish, then transfer it in the background')
    x.add_argument('--wait-idle', action='store_true', help=argparse.SUPPRESS)
    x.add_argument('--run-id', help=argparse.SUPPRESS)
    a = p.parse_args()
    if a.command == 'worker':
        result = worker(json.load(sys.stdin))
    elif a.command == 'move':
        if a.detach:
            rid = uuid.uuid4().hex
            log = '/tmp/teleport-' + rid + '.log'
            args = [x for x in sys.argv[1:] if x != '--detach'] + ['--wait-idle', '--run-id', rid]
            with open(log, 'x') as f:
                child = subprocess.Popen([sys.executable, str(SELF), *args], stdin=subprocess.DEVNULL,
                                         stdout=f, stderr=f, start_new_session=True)
            result = {'status': 'scheduled', 'run_id': rid, 'pid': child.pid, 'log': log}
        else:
            try:
                result = transfer(a)
            except Exception as e:
                if a.run_id:
                    path = ROOT / 'runs' / a.run_id / 'transfer.json'
                    if path.exists():
                        failed = json.loads(path.read_text())
                        failed.update(status='failed', error=str(e))
                        save(path, failed)
                raise
    else:
        result = endpoint(a.host, a.command, vars(a))
        if a.command == 'launch':
            record = ROOT / 'runs' / a.run_id / 'transfer.json'
            if record.exists():
                state = json.loads(record.read_text())
                if state.get('destination') == a.host:
                    state.update(status=result['status'], result=result)
                    state.pop('error', None)
                    save(record, state)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(json.dumps({'status': 'failed', 'error': str(e)}), file=sys.stderr)
        sys.exit(1)
