#!/usr/bin/env python3
"""Install the local command; skill discovery uses the existing dotfiles links."""
from pathlib import Path

target = Path.home() / '.local/bin/teleport'
content = '#!/bin/sh\nexec python3 "$HOME/.dotfiles/agents/skills/teleport/scripts/teleport.py" "$@"\n'
if target.exists() and target.read_text() != content:
    raise SystemExit(f'Refusing to replace an unrelated command: {target}')
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(content)
target.chmod(0o755)
print(target)
