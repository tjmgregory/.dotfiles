---
name: uploading-to-electric-sheep
description: Pulls videos or photos from the macOS Photos library for a date range (downloading iCloud-only originals) and uploads them into a named folder on Theo's Electric Sheep account via its API, then verifies nothing is missing or duplicated. Use when the user asks to get weekend clips, footage, videos or photos "up to Electric Sheep", "into my electric sheep account", or into an Electric Sheep folder, or mentions dev-edit.electricsheep.tv.
---

# Uploading to Electric Sheep

Two steps, both scripted: export from Photos, then upload and verify against the folder.

Requirements: `osxphotos` on PATH (`uv tool install osxphotos`), `op` CLI signed in, `curl`. Run `es_api.py` with the Bash sandbox disabled, because `op` cannot reach the desktop app from inside it.

Dev is the intended target (`dev-edit.electricsheep.tv`), not a mislabel. See [references/api_reference.md](references/api_reference.md) for endpoints, auth and quirks before doing anything the scripts do not cover.

## Workflow

1. Pin the dates. "The weekend 29/30th" means the most recent Saturday and Sunday with those day numbers. Confirm the year from today's date, do not ask.

2. Export from Photos into a scratch directory. Videos are the default; pass `"kind": "photos"` or `"all"` if asked.
   ```bash
   scripts/export_media.py <<'EOF'
   {"from": "2026-08-29", "to": "2026-08-30", "dest": "<scratchpad>/export"}
   EOF
   ```
   Read the JSON: `exported` should equal `processed`, `missing` and `errors` empty. Photos keeps originals in iCloud only, so the download is expected and takes a few minutes per GB. Run it in the background.

3. Create or find the folder. Use the user's exact wording for the name.
   ```bash
   scripts/es_api.py <<'EOF'
   {"op": "create_folder", "path": "tourist weekend with Alex"}
   EOF
   ```
   Keep the returned `id`.

4. Upload. Safe to rerun: titles already in the folder are skipped. Run in the background for anything over a few hundred MB.
   ```bash
   scripts/es_api.py <<'EOF'
   {"op": "upload", "dir": "<scratchpad>/export", "folder_id": "<id>"}
   EOF
   ```

5. Verify. `missing` and `duplicates` must be empty. `remote_with_children` is about double `remote` because the platform adds an `_audio` child per video; that is normal.
   ```bash
   scripts/es_api.py <<'EOF'
   {"op": "verify", "dir": "<scratchpad>/export", "folder_id": "<id>"}
   EOF
   ```
   If an uploader restart left duplicates, delete the extra ids with `{"op": "delete", "media_ids": [...]}`.

6. Report: clip count, total size, folder name, anything still `processing`. Leave the export directory in the scratchpad.

## Gotchas

- Do not probe the upload endpoint with real files to learn its fields. The fields are documented in the reference. If a probe is unavoidable, use a `text/plain` file, which is rejected before anything is stored.
- `GET /media?folder_id=` does not filter reliably. The scripts filter on `folder_path` client-side; do the same in any ad-hoc call.
- `osxphotos --to-date` is exclusive. `export_media.py` already adds a day, so pass the last wanted day as `to`.
