#!/usr/bin/env python3
"""Electric Sheep media API client. One op per call, JSON in on stdin, JSON out on stdout.

Ops:
  {"op": "folders"}                                      list folders (name, id, media_count)
  {"op": "create_folder", "path": "name"}                create (or return existing) folder, gives id
  {"op": "upload", "dir": "/path", "folder_id": "uuid"}  upload every video/audio/image file in dir
        optional: "titles_from": "stem" (default) | "filename"
        skips titles already in the folder, so reruns are safe; writes <dir>/uploads.json
  {"op": "verify", "dir": "/path", "folder_id": "uuid"}  compare dir contents with folder contents
  {"op": "delete", "media_ids": ["uuid", ...]}           delete media items
  {"op": "delete_folder", "folder_id": "uuid"}           delete a folder (use only for empty test folders)

Auth: reads the Bearer key from 1Password (item ID below) unless ES_API_KEY is set.
`op` fails inside the Bash sandbox, so run with the sandbox disabled.
Uses curl for uploads (multipart streaming of multi-GB files without extra deps).
"""
import json
import os
import subprocess
import sys
import time

BASE = "https://dev-edit.electricsheep.tv/api/v1"  # dev on purpose: investor access, see SKILL.md
OP_ITEM = "iu5v37zthenhj6tucyfoxi6j7e"  # 1Password TSE item "claude-m2-mac - electric-sheep"
MEDIA_EXT = (".mov", ".mp4", ".m4v", ".mp3", ".m4a", ".wav", ".jpg", ".jpeg", ".png", ".heic")


def out(obj):
    print(json.dumps(obj, indent=1))


def fail(msg):
    out({"error": msg})
    sys.exit(1)


def api_key():
    if os.environ.get("ES_API_KEY"):
        return os.environ["ES_API_KEY"]
    r = subprocess.run(["op", "item", "get", OP_ITEM, "--fields", "password", "--reveal"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        fail(f"op failed (run with sandbox off): {r.stderr.strip()}")
    return r.stdout.strip()


KEY = None


def call(method, path, *curl_args):
    global KEY
    KEY = KEY or api_key()
    r = subprocess.run(["curl", "-s", "-X", method, "-H", f"Authorization: Bearer {KEY}",
                        *curl_args, BASE + path], capture_output=True, text=True)
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return {"error": r.stdout.strip() or r.stderr.strip() or "empty response"}


def folder_items(folder_id):
    """All media whose folder_path contains folder_id. Cursor-paged."""
    items, cursor = [], None
    while True:
        d = call("GET", f"/media?folder_id={folder_id}&limit=100" + (f"&cursor={cursor}" if cursor else ""))
        if "data" not in d:
            fail(f"media list failed: {d}")
        items += [m for m in d["data"] if folder_id in (m.get("folder_path") or [])]
        if not d.get("has_more"):
            return items
        cursor = d["next_cursor"]


def local_files(d):
    if not os.path.isdir(d):
        fail(f"not a directory: {d}")
    return sorted(f for f in os.listdir(d) if f.lower().endswith(MEDIA_EXT))


def title_of(name, mode):
    return name if mode == "filename" else os.path.splitext(name)[0]


def op_folders(_):
    d = call("GET", "/folders")
    if "data" not in d:
        fail(f"folders failed: {d}")

    def flat(fs):
        for f in fs:
            yield {"name": f["name"], "path": f["path"], "id": f["id"], "media_count": f["media_count"]}
            yield from flat(f.get("children", []))
    out({"folders": list(flat(d["data"]))})


def op_create_folder(cfg):
    path = cfg.get("path") or fail("path required")
    d = call("GET", "/folders")
    for f in d.get("data", []):
        if f["path"] == path:
            out({"id": f["id"], "path": path, "created": False})
            return
    d = call("POST", "/folders", "-H", "Content-Type: application/json", "-d", json.dumps({"path": path}))
    if "id" not in d:
        fail(f"create failed: {d}")
    out({"id": d["id"], "path": d["path"], "created": True})


def op_upload(cfg):
    d, fid = cfg.get("dir") or fail("dir required"), cfg.get("folder_id") or fail("folder_id required")
    mode = cfg.get("titles_from", "stem")
    files = local_files(d)
    existing = {m["title"]: m["media_id"] for m in folder_items(fid)}
    log = os.path.join(d, "uploads.json")
    results = json.load(open(log)) if os.path.exists(log) else {}
    for i, name in enumerate(files, 1):
        title = title_of(name, mode)
        if title in existing:
            results[name] = {"media_id": existing[title], "skipped": True}
            print(f"[{i}/{len(files)}] skip {name}, already in folder", file=sys.stderr)
            continue
        path = os.path.join(d, name)
        t0 = time.time()
        r = {}
        for attempt in range(1, 4):  # transient failures on big files; three tries is plenty
            r = call("POST", "/media/upload", "-F", f"file=@{path}", "-F", f"folder_id={fid}", "-F", f"title={title}")
            if r.get("media_id"):
                break
            print(f"    attempt {attempt} failed: {r}", file=sys.stderr)
            time.sleep(5 * attempt)
        results[name] = {"media_id": r.get("media_id"), "size": os.path.getsize(path), "response": r}
        json.dump(results, open(log, "w"), indent=1)
        print(f"[{i}/{len(files)}] {name} {os.path.getsize(path)/1e6:.1f}MB -> {r.get('media_id')} "
              f"({time.time()-t0:.0f}s)", file=sys.stderr)
    failed = [n for n, v in results.items() if not v.get("media_id")]
    skipped = [n for n, v in results.items() if v.get("skipped")]
    out({"status": "ok" if not failed else "partial", "uploaded": len(files) - len(failed) - len(skipped),
         "skipped": len(skipped), "failed": failed, "log": log})


def op_verify(cfg):
    d, fid = cfg.get("dir") or fail("dir required"), cfg.get("folder_id") or fail("folder_id required")
    mode = cfg.get("titles_from", "stem")
    local = {title_of(f, mode) for f in local_files(d)}
    items = folder_items(fid)
    # The platform adds a "<title>_audio" child per video; ignore those when comparing.
    parents = [m for m in items if not m["title"].endswith("_audio")]
    titles = [m["title"] for m in parents]
    dupes = sorted({t for t in titles if titles.count(t) > 1})
    status = {}
    for m in parents:
        status[m["status"]] = status.get(m["status"], 0) + 1
    out({
        "status": "ok" if not (local - set(titles)) and not dupes else "mismatch",
        "local": len(local), "remote": len(parents), "remote_with_children": len(items),
        "missing": sorted(local - set(titles)),
        "extra": sorted(set(titles) - local),
        "duplicates": dupes,
        "processing_status": status,
    })


def op_delete(cfg):
    ids = cfg.get("media_ids") or fail("media_ids required")
    out({"deleted": {mid: call("DELETE", f"/media/{mid}") for mid in ids}})


def op_delete_folder(cfg):
    fid = cfg.get("folder_id") or fail("folder_id required")
    out(call("DELETE", f"/folders/{fid}"))


OPS = {"folders": op_folders, "create_folder": op_create_folder, "upload": op_upload,
       "verify": op_verify, "delete": op_delete, "delete_folder": op_delete_folder}

if sys.stdin.isatty():
    fail('needs JSON on stdin, e.g. {"op":"folders"}')
cfg = json.load(sys.stdin)
op = cfg.get("op")
if op not in OPS:
    fail(f"op must be one of {sorted(OPS)}")
OPS[op](cfg)
