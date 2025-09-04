# .dotfiles

Symlink things, i.e.

```sh
ln -s ~/.dotfiles/helix ~/.config/helix
ln -s ~/.dotfiles/karabiner ~/.config/karabiner
```

## Worktree Management

This dotfiles setup includes a comprehensive worktree management system. For detailed documentation, see [`ai/worktrees.md`](ai/worktrees.md).

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

For complete usage instructions, architecture details, and integration guides, see the [full WorkTrees documentation](ai/worktrees.md).
