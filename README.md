# .dotfiles

Symlink things, i.e.

```sh
ln -s ~/.dotfiles/helix ~/.config/helix
ln -s ~/.dotfiles/karabiner ~/.config/karabiner
```

## Worktree Management

This dotfiles setup includes a worktree management system that stores worktrees in each repository's `.worktrees` directory. This approach:

- Keeps worktrees organized within each repository
- Avoids conflicts with Git's internal worktree management
- Uses a global gitignore to ignore `.worktrees` folders
- Provides clean separation between repositories

### Usage

The `wt` script provides worktree management:

```sh
# Create a new worktree
wt create ~/work/elephant/my-repo feature-branch

# List all worktrees
wt list

# List worktrees for a specific repo
wt list my-repo

# Remove a worktree
wt remove my-repo feature-branch

# Switch to a worktree directory
wt cd my-repo feature-branch

# Clean up orphaned worktrees
wt clean
```

### Directory Structure

Worktrees are stored as:
```
~/work/elephant/my-repo/
├── .git/                    # Main repository
├── .worktrees/             # Worktrees directory (gitignored)
│   ├── feature-branch/     # Worktree for feature-branch
│   └── bugfix-123/         # Worktree for bugfix-123
└── ...                     # Main repository files
```

### VS Code Integration

Configure the Git Worktree Manager extension with:
- **Worktree Path Template**: `$BASE_PATH/.worktrees`
- **Worktree Subdirectory Template**: `$INDEX`
