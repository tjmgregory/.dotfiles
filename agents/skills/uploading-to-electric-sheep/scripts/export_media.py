#!/usr/bin/env python3
"""Export media from the macOS Photos library by date, downloading iCloud-only originals.

Input (JSON on stdin):
  {"from": "2026-08-29", "to": "2026-08-30", "dest": "/path/to/dir",
   "kind": "videos"}            # kind: videos (default) | photos | all

Output (JSON on stdout): {"status", "dest", "processed", "exported", "missing", "errors", "files": [...]}
Progress goes to stderr. Requires `osxphotos` on PATH (uv tool install osxphotos).
"""
import datetime as dt
import json
import os
import shutil
import subprocess
import sys


def fail(msg):
    print(json.dumps({"error": msg}))
    sys.exit(1)


if sys.stdin.isatty():
    fail('needs JSON on stdin, e.g. {"from":"2026-08-29","to":"2026-08-30","dest":"./export"}')

cfg = json.load(sys.stdin)
for k in ("from", "to", "dest"):
    if k not in cfg:
        fail(f"missing field: {k}")
if not shutil.which("osxphotos"):
    fail("osxphotos not on PATH; install with: uv tool install osxphotos")

# osxphotos --to-date is exclusive, so push it one day past the last wanted day.
to_excl = (dt.date.fromisoformat(cfg["to"]) + dt.timedelta(days=1)).isoformat()
dest = os.path.abspath(cfg["dest"])
os.makedirs(dest, exist_ok=True)

kind_flag = {"videos": ["--only-movies"], "photos": ["--only-photos"], "all": []}
kind = cfg.get("kind", "videos")
if kind not in kind_flag:
    fail("kind must be videos, photos or all")

report = os.path.join(dest, "export-report.json")
cmd = [
    "osxphotos", "export", dest,
    "--from-date", cfg["from"], "--to-date", to_excl,
    "--download-missing", "--use-photokit",   # pull iCloud-only originals
    "--skip-live", "--skip-edited",            # originals only, no live-photo movies or edited copies
    "--no-progress", "--report", report,
    *kind_flag[kind],
]
print("running: " + " ".join(cmd), file=sys.stderr)
proc = subprocess.run(cmd, capture_output=True, text=True)
tail = "\n".join(proc.stdout.strip().splitlines()[-3:])
print(tail, file=sys.stderr)
if proc.returncode != 0:
    fail(f"osxphotos exit {proc.returncode}: {proc.stderr.strip()[-500:]}")

rows = json.load(open(report)) if os.path.exists(report) else []
exported = [os.path.basename(r["filename"]) for r in rows if r.get("exported")]
missing = [os.path.basename(r["filename"]) for r in rows if r.get("missing")]
errors = [os.path.basename(r["filename"]) for r in rows if r.get("error")]
print(json.dumps({
    "status": "ok" if not (missing or errors) else "partial",
    "dest": dest,
    "processed": len(rows),
    "exported": len(exported),
    "missing": missing,
    "errors": errors,
    "files": sorted(exported),
}))
