#!/usr/bin/env python3
"""
Promote Skill - Make a project-local skill globally available

Creates a symlink in the global skills directory pointing to a project skill,
making it available to all IDEs without moving the source of truth.

Usage:
    promote_skill.py <skill-path>

Example:
    promote_skill.py ~/projects/my-app/skills/my-helper

Creates:
    ~/.dotfiles/agents/skills/my-helper -> ~/projects/my-app/skills/my-helper
"""

import sys
from pathlib import Path

GLOBAL_SKILLS_PATH = Path.home() / ".dotfiles/agents/skills"


def promote_skill(skill_path):
    """
    Promote a project skill to global availability via symlink.

    Args:
        skill_path: Path to the project skill directory

    Returns:
        True if successful, False otherwise
    """
    skill_path = Path(skill_path).resolve()

    # Validate skill exists
    if not skill_path.exists():
        print(f"Error: Skill path does not exist: {skill_path}")
        return False

    if not skill_path.is_dir():
        print(f"Error: Skill path is not a directory: {skill_path}")
        return False

    # Validate it's actually a skill (has SKILL.md)
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"Error: No SKILL.md found in {skill_path}")
        print("       This doesn't appear to be a valid skill directory.")
        return False

    # Validate global skills directory exists
    if not GLOBAL_SKILLS_PATH.exists():
        print(f"Error: Global skills directory not found: {GLOBAL_SKILLS_PATH}")
        return False

    # Check if already promoted
    skill_name = skill_path.name
    global_link = GLOBAL_SKILLS_PATH / skill_name

    if global_link.is_symlink():
        current_target = global_link.resolve()
        if current_target == skill_path:
            print(f"Already promoted: {skill_name}")
            print(f"  {global_link} -> {skill_path}")
            return True
        else:
            print(f"Error: {global_link} already exists but points to {current_target}")
            print(f"       Expected: {skill_path}")
            return False
    elif global_link.exists():
        print(f"Error: {global_link} already exists and is not a symlink")
        print("       A global skill with this name already exists.")
        return False

    # Create the symlink
    global_link.symlink_to(skill_path)
    print(f"Promoted: {skill_name}")
    print(f"  {global_link} -> {skill_path}")
    print(f"\nSkill '{skill_name}' is now globally available to all IDEs.")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: promote_skill.py <skill-path>")
        print("\nMakes a project-local skill globally available via symlink.")
        print("\nExample:")
        print("  promote_skill.py ~/projects/my-app/skills/my-helper")
        print("\nCreates:")
        print(f"  {GLOBAL_SKILLS_PATH}/<skill-name> -> <skill-path>")
        print("\nThe skill remains in the project (source of truth) but becomes")
        print("available to all IDEs through the global skills directory.")
        sys.exit(1)

    skill_path = sys.argv[1]

    if promote_skill(skill_path):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
