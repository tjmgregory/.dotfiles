# Verification — 2026-09-20

Installed on M2 and M1 (`m1srv`), with shared Codex/Claude skill discovery and `~/.local/bin/teleport`.

Passed with disposable conversations:
- Codex 0.154.0 M2 → M1 → M2: native history and remembered fixture facts survived both directions.
- Claude Code 2.1.267 / 2.1.257 M2 → M1 → M2: native history and remembered fixture facts survived both directions.
- Codex → Claude: destination read the handover and source transcript, recovered fixture facts and unfinished file contents.
- Claude → Codex: durable thread imported and resumed. Tool-based handover reading remains blocked by the M1 runtime issue below.
- Automated tests: Git index, unstaged/binary/deleted/untracked files, collision protection, archive traversal/symlink rejection, checksum corruption, and destination preflight before source export.
- Skill schema validation.

M1 limitation: the signed bundled `codex-code-mode-host` hangs before program startup; fresh Codex CLI sessions also cannot execute tools. Signature verification and SHA256 match the working M2 helper. Removing the helper's quarantine and replacing it with an identical verified copy did not resolve the installed-path failure. No security service or global security policy was changed. Original helper backup: `/tmp/teleport-code-mode-host-original`. Teleport now refuses Codex transfers to a machine whose helper fails its 10-second startup check. Claude transfers remain available. Run `teleport doctor --host m1srv` after repairing Codex.

Detached self-transfer scheduling is implemented but not end-to-end validated. No production deployment actions were performed. Original user chats remain at their original IDs and locations; the early deployment verification copy was closed and archived at the user's clarification. Recovery bundles are retained. Nothing in `/tmp` was cleaned.
