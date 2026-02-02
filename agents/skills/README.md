# Agent Skills

Skills following the [Agent Skills](https://agentskills.io/) open standard.

This format is supported by Claude Code, Cursor, VS Code, Gemini CLI, and other agent tools.

## Structure

Each skill is a folder containing a `SKILL.md` file with instructions the agent loads on demand.

```
skills/
├── conventional-commit/SKILL.md
├── find-skills/SKILL.md
├── skill-creator/SKILL.md
└── bd-issue-tracking -> ~/projects/beads/...
```

## Symlinks

- `~/.claude/skills` → this directory
- `~/.cursor/skills` → this directory

## Resources

- [Specification](https://agentskills.io/specification)
- [Example skills](https://github.com/anthropics/skills)
