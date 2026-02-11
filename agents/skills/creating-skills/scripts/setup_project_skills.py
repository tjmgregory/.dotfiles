#!/usr/bin/env python3
"""
Setup Project Skills - Configure a project directory for local skills

Creates the skills/ directory and IDE symlinks so that project-local skills
are discoverable by Claude Code, Cursor, and other IDEs.

Usage (CLI args):
    setup_project_skills.py <project-path>

Usage (JSON stdin - preferred for AI agents):
    setup_project_skills.py <<'EOF'
    {"path": "~/projects/my-app"}
    EOF

JSON input fields:
    path/project_path: Path to project directory (required)

Outputs JSON to stdout:
    Success: {"status": "ok", "path": "/path/to/project", "skills_dir": "/path/to/project/skills"}
    Error:   {"error": "message"}

Creates:
    <project>/skills/              # Skills directory (if missing)
    <project>/.claude/skills → skills  # Symlink for Claude Code
    <project>/.cursor/skills → skills  # Symlink for Cursor
"""

import sys
import json
from pathlib import Path


def output_json(data: dict) -> None:
    """Output structured JSON to stdout."""
    print(json.dumps(data))

# IDE configurations: (config_dir, skills_subdir)
IDE_CONFIGS = [
    (".claude", "skills"),
    (".cursor", "skills"),
]


def setup_project_skills(project_path):
    """
    Set up a project directory for local skills.

    Args:
        project_path: Path to the project root

    Returns:
        Tuple of (skills_dir path, error message) - one will be None
    """
    project_path = Path(project_path).resolve()

    if not project_path.exists():
        return None, f"Project path does not exist: {project_path}"

    if not project_path.is_dir():
        return None, f"Path is not a directory: {project_path}"

    # Create skills directory if it doesn't exist
    skills_dir = project_path / "skills"
    if not skills_dir.exists():
        skills_dir.mkdir()
        print(f"Created: {skills_dir}", file=sys.stderr)
    else:
        print(f"Exists:  {skills_dir}", file=sys.stderr)

    # Set up symlinks for each IDE
    for config_dir, skills_subdir in IDE_CONFIGS:
        ide_config_path = project_path / config_dir
        ide_skills_link = ide_config_path / skills_subdir

        # Create IDE config directory if needed
        if not ide_config_path.exists():
            ide_config_path.mkdir()
            print(f"Created: {ide_config_path}", file=sys.stderr)

        # Create or verify symlink
        if ide_skills_link.is_symlink():
            current_target = ide_skills_link.resolve()
            if current_target == skills_dir:
                print(f"Exists:  {ide_skills_link} -> skills", file=sys.stderr)
            else:
                print(f"Warning: {ide_skills_link} points to {current_target}, expected {skills_dir}", file=sys.stderr)
        elif ide_skills_link.exists():
            print(f"Warning: {ide_skills_link} exists but is not a symlink", file=sys.stderr)
        else:
            # Create relative symlink: .claude/skills -> ../skills
            relative_target = Path("..") / "skills"
            ide_skills_link.symlink_to(relative_target)
            print(f"Created: {ide_skills_link} -> {relative_target}", file=sys.stderr)

    print(f"Project '{project_path.name}' is now configured for local skills.", file=sys.stderr)
    print(f"Create skills in: {skills_dir}/", file=sys.stderr)
    return skills_dir, None


def parse_args():
    """Parse arguments from stdin JSON or CLI args."""
    # Check for JSON input via stdin (AI-friendly mode)
    if not sys.stdin.isatty():
        try:
            data = json.load(sys.stdin)
            path = data.get("path") or data.get("project_path")
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
        print("Usage: setup_project_skills.py <project-path>", file=sys.stderr)
        output_json({"error": "Usage: setup_project_skills.py <project-path>"})
        sys.exit(1)

    return sys.argv[1]


def main():
    project_path = parse_args()

    print(f"Setting up project for local skills: {project_path}", file=sys.stderr)

    skills_dir, error = setup_project_skills(project_path)

    if skills_dir:
        output_json({
            "status": "ok",
            "path": str(Path(project_path).resolve()),
            "skills_dir": str(skills_dir)
        })
        sys.exit(0)
    else:
        output_json({"error": error})
        sys.exit(1)


if __name__ == "__main__":
    main()
