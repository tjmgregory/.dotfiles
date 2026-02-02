# .dotfiles

Symlink things, i.e.

```sh
ln -s ~/.dotfiles/helix ~/.config/helix
ln -s ~/.dotfiles/karabiner ~/.config/karabiner
ln -s ~/.dotfiles/claude/CLAUDE.md ~/.claude/CLAUDE.md
ln -s ~/.dotfiles/claude/settings.json ~/.claude/settings.json
ln -s ~/.dotfiles/claude/skills ~/.claude/skills
```

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
