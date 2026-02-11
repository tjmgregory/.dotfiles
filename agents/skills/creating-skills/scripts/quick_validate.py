#!/usr/bin/env python3
"""
Quick validation script for skills - minimal version

Usage (CLI args):
    quick_validate.py <skill_directory>

Usage (JSON stdin - preferred for AI agents):
    quick_validate.py <<'EOF'
    {"path": "/path/to/skill"}
    EOF

Outputs JSON to stdout:
    Success: {"status": "ok", "valid": true, "message": "Skill is valid!"}
    Invalid: {"status": "ok", "valid": false, "message": "Error description"}
    Error:   {"error": "message"}
"""

import sys
import os
import re
import json
import yaml
from pathlib import Path


def output_json(data: dict) -> None:
    """Output structured JSON to stdout."""
    print(json.dumps(data))

def validate_skill(skill_path):
    """Basic validation of a skill"""
    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found"

    # Read and validate frontmatter
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "No YAML frontmatter found"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    # Parse YAML frontmatter
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    # Define allowed properties
    ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata'}

    # Check for unexpected properties (excluding nested keys under metadata)
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # Check required fields
    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    # Extract name for validation
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        # Check naming convention (hyphen-case: lowercase with hyphens)
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
        # Check name length (max 64 characters per spec)
        if len(name) > 64:
            return False, f"Name is too long ({len(name)} characters). Maximum is 64 characters."

    # Extract and validate description
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if description:
        # Check for angle brackets
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets (< or >)"
        # Check description length (max 1024 characters per spec)
        if len(description) > 1024:
            return False, f"Description is too long ({len(description)} characters). Maximum is 1024 characters."

    return True, "Skill is valid!"

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
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>", file=sys.stderr)
        output_json({"error": "Usage: quick_validate.py <skill_directory>"})
        sys.exit(1)

    return sys.argv[1]


if __name__ == "__main__":
    skill_path = parse_args()
    valid, message = validate_skill(skill_path)

    print(message, file=sys.stderr)
    output_json({
        "status": "ok",
        "valid": valid,
        "message": message,
        "path": str(skill_path)
    })
    sys.exit(0 if valid else 1)