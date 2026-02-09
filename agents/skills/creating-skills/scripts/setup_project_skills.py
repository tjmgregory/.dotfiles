#!/usr/bin/env python3
"""
Setup Project Skills - Configure a project directory for local skills

Creates the skills/ directory and IDE symlinks so that project-local skills
are discoverable by Claude Code, Cursor, and other IDEs.

Usage:
    setup_project_skills.py <project-path>

Example:
    setup_project_skills.py ~/projects/my-app

Creates:
    <project>/skills/              # Skills directory (if missing)
    <project>/.claude/skills → skills  # Symlink for Claude Code
    <project>/.cursor/skills → skills  # Symlink for Cursor
"""

import sys
from pathlib import Path

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
        True if successful, False otherwise
    """
    project_path = Path(project_path).resolve()

    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}")
        return False

    if not project_path.is_dir():
        print(f"Error: Path is not a directory: {project_path}")
        return False

    # Create skills directory if it doesn't exist
    skills_dir = project_path / "skills"
    if not skills_dir.exists():
        skills_dir.mkdir()
        print(f"Created: {skills_dir}")
    else:
        print(f"Exists:  {skills_dir}")

    # Set up symlinks for each IDE
    for config_dir, skills_subdir in IDE_CONFIGS:
        ide_config_path = project_path / config_dir
        ide_skills_link = ide_config_path / skills_subdir

        # Create IDE config directory if needed
        if not ide_config_path.exists():
            ide_config_path.mkdir()
            print(f"Created: {ide_config_path}")

        # Create or verify symlink
        if ide_skills_link.is_symlink():
            current_target = ide_skills_link.resolve()
            if current_target == skills_dir:
                print(f"Exists:  {ide_skills_link} -> skills")
            else:
                print(f"Warning: {ide_skills_link} points to {current_target}, expected {skills_dir}")
        elif ide_skills_link.exists():
            print(f"Warning: {ide_skills_link} exists but is not a symlink")
        else:
            # Create relative symlink: .claude/skills -> ../skills
            relative_target = Path("..") / "skills"
            ide_skills_link.symlink_to(relative_target)
            print(f"Created: {ide_skills_link} -> {relative_target}")

    print(f"\nProject '{project_path.name}' is now configured for local skills.")
    print(f"Create skills in: {skills_dir}/")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: setup_project_skills.py <project-path>")
        print("\nSets up IDE symlinks so project-local skills are discoverable.")
        print("\nExample:")
        print("  setup_project_skills.py ~/projects/my-app")
        print("\nCreates:")
        print("  <project>/skills/              # Skills directory")
        print("  <project>/.claude/skills -> skills")
        print("  <project>/.cursor/skills -> skills")
        sys.exit(1)

    project_path = sys.argv[1]

    print(f"Setting up project for local skills: {project_path}\n")

    if setup_project_skills(project_path):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
