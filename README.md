# .dotfiles

Symlink things:

```sh
# General
ln -s ~/.dotfiles/helix ~/.config/helix
ln -s ~/.dotfiles/karabiner ~/.config/karabiner

# Claude Code
ln -s ~/.dotfiles/claude/CLAUDE.md ~/.claude/CLAUDE.md
ln -s ~/.dotfiles/claude/settings.json ~/.claude/settings.json
ln -s ~/.dotfiles/agents/skills ~/.claude/skills

# Cursor
ln -s ~/.dotfiles/agents/skills ~/.cursor/skills
```

Skills are consolidated in `agents/skills/` following the [agentskills.io](https://agentskills.io/) standard and shared between Claude and Cursor.

## Claude Code marketplace

This repo is also published as a [Claude Code plugin marketplace](https://docs.claude.com/en/docs/claude-code/plugins) so individual skills can be installed by anyone:

```
/plugin marketplace add tjmgregory/.dotfiles
/plugin install <name>@tjmgregory
```

### Installable skills

| Name | What it does |
|---|---|
| [`human-friendly`](agents/skills/human-friendly) | Renders the next plan/design as an editable HTML doc on your Desktop instead of chat markdown — `designMode` editing, ⌘S file-save, markdown shortcuts, hover add-row/col on tables, live reload. |

See [`.claude-plugin/README.md`](.claude-plugin/README.md) for publication conventions.

## Worktree Management

This dotfiles setup includes a comprehensive worktree management system using Git worktrees for parallel development.

### Quick Reference

The `wt` script provides worktree management:

```sh
# Create and switch to a worktree
wt cd my-repo feature-branch

# List all worktrees
wt list

# Remove a worktree
wt remove my-repo feature-branch

# Clean up orphaned worktrees
wt clean
```

### Documentation

- **[WorkTrees Workflow Guide](ai/worktrees.md)** - Conceptual understanding and workflow patterns
- **[WT Script Documentation](bin/wt.md)** - Detailed command reference and implementation
