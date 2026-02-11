#!/usr/bin/env python3
"""
Promote Skill - Make a project-local skill globally available

Creates a symlink in the global skills directory pointing to a project skill,
making it available to all IDEs without moving the source of truth.

Usage (CLI args):
    promote_skill.py <skill-path>

Usage (JSON stdin - preferred for AI agents):
    promote_skill.py <<'EOF'
    {"path": "~/projects/my-app/skills/my-helper"}
    EOF

JSON input fields:
    path/skill_path: Path to project skill directory (required)

Outputs JSON to stdout:
    Success: {"status": "ok", "name": "my-helper", "link": "/global/path", "target": "/project/path"}
    Error:   {"error": "message"}

Creates:
    ~/.dotfiles/agents/skills/my-helper -> ~/projects/my-app/skills/my-helper
"""

import sys
import json
from pathlib import Path


def output_json(data: dict) -> None:
    """Output structured JSON to stdout."""
    print(json.dumps(data))

GLOBAL_SKILLS_PATH = Path.home() / ".dotfiles/agents/skills"


def promote_skill(skill_path):
    """
    Promote a project skill to global availability via symlink.

    Args:
        skill_path: Path to the project skill directory

    Returns:
        Tuple of (result dict, error message) - one will be None
    """
    skill_path = Path(skill_path).resolve()

    # Validate skill exists
    if not skill_path.exists():
        return None, f"Skill path does not exist: {skill_path}"

    if not skill_path.is_dir():
        return None, f"Skill path is not a directory: {skill_path}"

    # Validate it's actually a skill (has SKILL.md)
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return None, f"No SKILL.md found in {skill_path}. This doesn't appear to be a valid skill directory."

    # Validate global skills directory exists
    if not GLOBAL_SKILLS_PATH.exists():
        return None, f"Global skills directory not found: {GLOBAL_SKILLS_PATH}"

    # Check if already promoted
    skill_name = skill_path.name
    global_link = GLOBAL_SKILLS_PATH / skill_name

    if global_link.is_symlink():
        current_target = global_link.resolve()
        if current_target == skill_path:
            print(f"Already promoted: {skill_name}", file=sys.stderr)
            print(f"  {global_link} -> {skill_path}", file=sys.stderr)
            return {"name": skill_name, "link": str(global_link), "target": str(skill_path), "already_existed": True}, None
        else:
            return None, f"{global_link} already exists but points to {current_target}, expected {skill_path}"
    elif global_link.exists():
        return None, f"{global_link} already exists and is not a symlink. A global skill with this name already exists."

    # Create the symlink
    global_link.symlink_to(skill_path)
    print(f"Promoted: {skill_name}", file=sys.stderr)
    print(f"  {global_link} -> {skill_path}", file=sys.stderr)
    print(f"Skill '{skill_name}' is now globally available to all IDEs.", file=sys.stderr)
    return {"name": skill_name, "link": str(global_link), "target": str(skill_path), "already_existed": False}, None


def parse_args():
    """Parse arguments from stdin JSON or CLI args."""
    # Check for JSON input via stdin (AI-friendly mode)
    if not sys.stdin.isatty():
        try:
            data = json.load(sys.stdin)
            path = data.get("path") or data.get("skill_path")
            if not path:
                print("Error: Missing required field 'path'", file=sys.stderr)
                output_json({"error": "Missing required field 'path'"})
                sys.exit(1)
            return path
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
            output_json({"error": f"Invalid JSON input: {e}"})
            sys.exit(1)

    # Fallback to CLI args
    if len(sys.argv) < 2:
        print("Usage: promote_skill.py <skill-path>", file=sys.stderr)
        output_json({"error": "Usage: promote_skill.py <skill-path>"})
        sys.exit(1)

    return sys.argv[1]


def main():
    skill_path = parse_args()

    result, error = promote_skill(skill_path)

    if result:
        output_json({"status": "ok", **result})
        sys.exit(0)
    else:
        output_json({"error": error})
        sys.exit(1)


if __name__ == "__main__":
    main()
