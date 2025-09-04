# WorkTrees Management System

## Overview

This dotfiles setup includes a comprehensive worktree management system that provides a standardized approach to managing Git worktrees across multiple repositories. The system stores worktrees in each repository's `.worktrees` directory, providing clean organization and avoiding conflicts with Git's internal worktree management.

## Architecture & Design Decisions

### Worktree Location Strategy
- **Location**: Each repository's `.worktrees` directory
- **Path**: `<repo-path>/.worktrees/<branch-name>/`

### Key Benefits
- Keeps worktrees organized within each repository
- Avoids conflicts with Git's internal worktree management
- Uses a global gitignore to ignore `.worktrees` folders
- Provides clean separation between repositories
- Easy to find and manage within each repository
- Works with both Crystal worktree managers and VS Code

## Directory Structure

Worktrees are stored as:
```
~/work/elephant/my-repo/
├── .git/                    # Main repository
├── .worktrees/             # Worktrees directory (gitignored)
│   ├── feature-branch/     # Worktree for feature-branch
│   └── bugfix-123/         # Worktree for bugfix-123
└── ...                     # Main repository files
```

## Management Script: `wt`

The `wt` script provides comprehensive worktree management functionality located at `~/.dotfiles/bin/wt`.

### Available Commands

```bash
# Create a new worktree
wt create <repo-path> <branch-name>

# List all worktrees
wt list

# List worktrees for a specific repo
wt list <repo-name>

# Remove a worktree
wt remove <repo-name> <branch-name>

# Switch to a worktree directory (creates if needed)
wt cd <repo-name> <branch-name>

# Clean up orphaned worktrees
wt clean
```

### Command Examples

```bash
# Create and switch to a new worktree
wt cd api-patient feature-auth

# Go to existing worktree
wt cd api-patient existing-branch

# List worktrees for specific repository
wt ls api-patient

# Remove a worktree
wt rm api-patient feature-auth

# Clean up orphaned worktrees
wt clean
```

## Implementation Details

### Worktree Creation Process
1. Creates the `.worktrees` directory if it doesn't exist
2. Attempts to create worktree from existing branch
3. If branch doesn't exist, creates new branch automatically
4. Provides clear feedback and error handling

### Repository Discovery
The script searches multiple directories for repositories:
- `~/work/elephant/` (job repositories)
- `~/projects/` (personal projects)
- Additional search paths as configured

### Error Handling & User Experience
- Color-coded output (INFO, SUCCESS, WARNING, ERROR)
- Interactive prompts for worktree creation
- Graceful handling of missing branches
- Automatic cleanup of orphaned worktrees

## VS Code Integration

Configure the Git Worktree Manager extension with:
- **Worktree Path Template**: `$BASE_PATH/.worktrees`
- **Worktree Subdirectory Template**: `$INDEX`

This allows VS Code to automatically discover and manage worktrees created by the `wt` script.

## Shell Integration

The system includes:
- Shell aliases for quick access
- PATH setup for the `wt` script
- Shell functions for seamless directory switching

## Migration & Standardization

The system has been standardized to:
- Store worktrees in each repository's `.worktrees` directory
- Migrate existing worktrees from scattered locations
- Configure VS Code to scan `.worktrees` directories within repositories
- Add shell aliases and PATH setup

## Best Practices

1. **Consistent Naming**: Use descriptive branch names that indicate the feature or fix
2. **Regular Cleanup**: Run `wt clean` periodically to remove orphaned worktrees
3. **Repository Organization**: Keep work repositories in `~/work/elephant/` and personal projects in `~/projects/`
4. **VS Code Integration**: Use the Git Worktree Manager extension for seamless IDE integration

## Troubleshooting

### Common Issues
- **Worktree already exists**: The script will detect existing worktrees and offer to switch to them
- **Branch doesn't exist**: The script will automatically create the branch if it doesn't exist
- **Orphaned worktrees**: Use `wt clean` to remove worktrees that no longer have corresponding branches

### Debugging
- Use `wt list` to see all current worktrees
- Check the `.worktrees` directory in your repository for physical worktree locations
- Verify VS Code settings if worktrees aren't appearing in the IDE

## Future Enhancements

Potential improvements identified:
- Enhanced AI context sharing across different tools
- Better integration with multiple AI assistants (Claude, Cursor, Crystal)
- Streamlined documentation workflow
- Centralized knowledge hub for preferences and workflow patterns
