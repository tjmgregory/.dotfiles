---
name: teleport
description: Move a Codex or Claude Code conversation and its unfinished Git work between machines through SSH and Herdr, or hand the task to the other assistant. Use for "teleport this chat", "move this conversation to M1/M2", "bring this chat back", or an explicit Codex-to-Claude handover.
---

# Teleport

Use the deterministic helper at `scripts/teleport.py`. Both Macs discover this shared skill through `~/.agents/skills` and `~/.claude/skills`.

Run `python3 ~/.dotfiles/agents/skills/teleport/scripts/teleport.py --help` for the installed interface. `m1srv` is the M1 SSH alias. `local` means the machine executing the helper. From the M2, push to M1 or pull from M1 through the existing SSH connection; reverse SSH access is not required.

## Select the exact conversation

- For a named saved chat: `teleport list --kind codex --query "relay"` (add `--host m1srv` for remote discovery).
- For a live chat, use the Herdr skill to read its exact pane and session IDs. Never guess from transcript modification time or select the most recent session in a shared directory.
- `teleport doctor --host m1srv` checks the destination, including whether the bundled Codex tool runtime starts. A failed runtime check blocks Codex transfers before the source exits. The source must finish its turn first. A verified idle source agent is exited before snapshotting; its pane and original history remain.
- For an umbrella directory with more than eight repositories, select the task's repositories explicitly with repeated `--repo NAME`. Include shared standards/instructions when the task depends on them. Do not transfer unrelated projects.

## Move and return

```sh
teleport move --to m1srv --kind codex --session EXACT_SESSION_ID
teleport move --from m1srv --to local --kind codex --session DESTINATION_SESSION_ID
```

Use `--kind claude` for Claude. `--pane EXACT_PANE_ID` can identify a live source instead of `--session`. `--as claude` or `--as codex` explicitly requests a cross-assistant handover. Omit `--as` to preserve the assistant.

When moving the conversation that is executing this skill, add `--detach`. The helper returns a transfer ID and a `/tmp` log, waits for this turn to finish, then exits the source agent and transfers it. Report **scheduled**, not ready, and end the turn so the transfer can proceed. Other conversations can use synchronous `move`. Never wait for your own detached transfer from inside the source conversation.

The destination inherits a Codex workspace trust decision only when the exact source cwd was trusted. `--trust-workspace` is available for a workspace whose contents are already approved (for example a test fixture you created); do not add it just to bypass an unknown repository's trust prompt.

Native transfers retain history under a new session ID. Cross-assistant transfers start a new conversation with a handover document and the original transcript; do not describe them as native resumption.

The helper restores work into `~/teleport-workspaces/<transfer-id>` and launches a named Herdr workspace without taking focus. It preserves commits, the Git index, unstaged and binary changes, and ordinary untracked files. Existing checkouts are not overwritten. Credentials, ignored files, dependencies, services, and running processes are not moved. Known credential filenames are excluded or rejected; this is not a general secret-content scanner. Report exclusions.

Read `TELEPORT-HANDOVER.md` in the destination before continuing. Earlier history references the old workspace; use the current workspace for edits. Recheck live deployment/service state before acting on old observations.

## Completion and recovery

Only report success when the helper returns `status: ready` with the verified destination session ID and Herdr pane. `imported` means files/history are restored but the terminal has not been verified. A startup permission or authentication prompt is not success; inspect it and handle it under the Herdr skill's rules.

```sh
teleport status --host m1srv TRANSFER_ID
teleport launch --host m1srv TRANSFER_ID
```

Records and immutable bundles are in `~/.local/share/teleport/runs/`. On failure, inspect the record before retrying; do not create duplicate destinations. The source history remains resumable with its original ID. Never overwrite an existing transcript or database to repair a transfer. Never clean `/tmp`.

For installation on another machine with the shared skill directory, run `python3 scripts/install.py`. Requires Python 3.11+, Git, SSH/SCP, Herdr, and the relevant authenticated assistant. Native Codex import is tested against 0.154.0: it registers a separate raw-history seed as legacy, then uses native fork to reconstruct a new session. It verifies every raw response item's content and order before launch. Other Codex versions must pass the round-trip test before being treated as compatible.

If the user only wants to view the existing remote terminal, use Herdr remote attachment instead of moving files or sessions. Execution stays on its original host.

Validation results and current machine limitations: `tests/verification.md`.
