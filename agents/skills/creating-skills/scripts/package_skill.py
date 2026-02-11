#!/usr/bin/env python3
"""
Skill Packager - Creates a distributable .skill file of a skill folder

Usage (CLI args):
    package_skill.py <path/to/skill-folder> [output-directory]

Usage (JSON stdin - preferred for AI agents):
    package_skill.py <<'EOF'
    {"path": "/path/to/skill", "output_dir": "./dist"}
    EOF

JSON input fields:
    path/skill_path: Path to skill folder (required)
    output_dir: Output directory for .skill file (optional)

Outputs JSON to stdout:
    Success: {"status": "ok", "path": "/path/to/skill.skill"}
    Error:   {"error": "message"}
"""

import sys
import json
import zipfile
from pathlib import Path
from quick_validate import validate_skill


def output_json(data: dict) -> None:
    """Output structured JSON to stdout."""
    print(json.dumps(data))


def package_skill(skill_path, output_dir=None):
    """
    Package a skill folder into a .skill file.

    Args:
        skill_path: Path to the skill folder
        output_dir: Optional output directory for the .skill file (defaults to current directory)

    Returns:
        Tuple of (Path to created .skill file, error message) - one will be None
    """
    skill_path = Path(skill_path).resolve()

    # Validate skill folder exists
    if not skill_path.exists():
        return None, f"Skill folder not found: {skill_path}"

    if not skill_path.is_dir():
        return None, f"Path is not a directory: {skill_path}"

    # Validate SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return None, f"SKILL.md not found in {skill_path}"

    # Run validation before packaging
    print("Validating skill...", file=sys.stderr)
    valid, message = validate_skill(skill_path)
    if not valid:
        return None, f"Validation failed: {message}"
    print(f"Validation passed: {message}", file=sys.stderr)

    # Determine output location
    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()

    skill_filename = output_path / f"{skill_name}.skill"

    # Create the .skill file (zip format)
    try:
        with zipfile.ZipFile(skill_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through the skill directory
            for file_path in skill_path.rglob('*'):
                if file_path.is_file():
                    # Calculate the relative path within the zip
                    arcname = file_path.relative_to(skill_path.parent)
                    zipf.write(file_path, arcname)
                    print(f"  Added: {arcname}", file=sys.stderr)

        print(f"Successfully packaged skill to: {skill_filename}", file=sys.stderr)
        return skill_filename, None

    except Exception as e:
        return None, f"Error creating .skill file: {e}"


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
            output_dir = data.get("output_dir")
            return path, output_dir
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
            output_json({"error": f"Invalid JSON input: {e}"})
            sys.exit(1)

    # Fallback to CLI args
    if len(sys.argv) < 2:
        print("Usage: package_skill.py <path/to/skill-folder> [output-directory]", file=sys.stderr)
        output_json({"error": "Usage: package_skill.py <path/to/skill-folder> [output-directory]"})
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    return skill_path, output_dir


def main():
    skill_path, output_dir = parse_args()

    print(f"Packaging skill: {skill_path}", file=sys.stderr)
    if output_dir:
        print(f"Output directory: {output_dir}", file=sys.stderr)

    result, error = package_skill(skill_path, output_dir)

    if result:
        output_json({"status": "ok", "path": str(result)})
        sys.exit(0)
    else:
        output_json({"error": error})
        sys.exit(1)


if __name__ == "__main__":
    main()
