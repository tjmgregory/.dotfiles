# WT Script Documentation

## Overview

The `wt` script is a comprehensive worktree management tool that provides standardized creation, listing, removal, and navigation of Git worktrees. It stores worktrees in each repository's `.worktrees` directory to maintain clean organization and avoid conflicts with Git's internal worktree management.

## Architecture

### Worktree Storage Strategy
- **Location**: `<repo-path>/.worktrees/<branch-name>/`
- **Benefits**: Keeps worktrees organized within each repository, avoids Git conflicts
- **Gitignore**: Uses global gitignore to ignore `.worktrees` folders

### Repository Discovery
The script searches multiple directories for repositories:
- `~/work/elephant/` (job repositories)
- `~/projects/` (personal projects)
- Additional search paths as configured

## Commands

### `wt cd <repo-name> <branch-name> [--print-path]`
**Primary command for worktree navigation and creation**

- **Purpose**: Switch to a worktree directory, creating it if it doesn't exist
- **Behavior**: 
  - If worktree exists: switches to it
  - If worktree doesn't exist: prompts to create it
  - If branch doesn't exist: creates new branch automatically
- **Options**:
  - `--print-path`: Only print the worktree path (used by shell functions)

**Examples**:
```bash
wt cd api-patient feature-auth        # Go to worktree (creates if needed)
wt cd api-patient existing-branch     # Go to existing worktree
```

### `wt list [repo-name]`
**List worktrees**

- **Purpose**: Display all worktrees or filter by repository
- **Behavior**:
  - No arguments: lists all worktrees across all repositories
  - With repo-name: lists worktrees for specific repository
- **Output**: Shows repository, branch name, and full path

**Examples**:
```bash
wt list                    # List all worktrees
wt list api-patient        # List worktrees for specific repo
```

### `wt remove <repo-name> <branch-name>`
**Remove a worktree**

- **Purpose**: Safely remove a worktree and clean up references
- **Behavior**:
  - Removes the worktree directory
  - Cleans up Git worktree references
  - Provides confirmation prompts

**Examples**:
```bash
wt remove api-patient feature-auth    # Remove specific worktree
```

### `wt clean`
**Clean up orphaned worktrees**

- **Purpose**: Remove worktrees that no longer have corresponding branches
- **Behavior**: Scans all repositories and removes orphaned worktrees

**Examples**:
```bash
wt clean                   # Clean up orphaned worktrees
```

## Implementation Details

### Worktree Creation Process
1. Validates repository exists and is a Git repository
2. Creates the `.worktrees` directory if it doesn't exist
3. Attempts to create worktree from existing branch
4. If branch doesn't exist, creates new branch automatically using `git worktree add -b`
5. Provides clear feedback and error handling

### Error Handling & User Experience
- **Color-coded output**: INFO (blue), SUCCESS (green), WARNING (yellow), ERROR (red)
- **Interactive prompts**: Asks for confirmation before creating worktrees
- **Graceful degradation**: Handles missing branches, repositories, and worktrees
- **Clear feedback**: Provides status updates for all operations

### Shell Integration
- **Shell functions**: Can be used by shell functions for directory switching
- **PATH setup**: Script is in PATH for global access
- **Aliases**: Can be aliased for shorter commands

## VS Code Integration

Configure the Git Worktree Manager extension with:
- **Worktree Path Template**: `$BASE_PATH/.worktrees`
- **Worktree Subdirectory Template**: `$INDEX`

This allows VS Code to automatically discover and manage worktrees created by the `wt` script.

## Usage Patterns

### Common Workflows

1. **Feature Development**:
   ```bash
   wt cd my-repo feature-auth    # Create and switch to feature branch
   # ... do work ...
   wt list my-repo              # Check worktrees
   ```

2. **Bug Fixes**:
   ```bash
   wt cd my-repo bugfix-123     # Create and switch to bugfix branch
   # ... fix bug ...
   wt remove my-repo bugfix-123 # Clean up when done
   ```

3. **Maintenance**:
   ```bash
   wt clean                     # Clean up orphaned worktrees
   wt list                      # Review all worktrees
   ```

## Troubleshooting

### Common Issues

1. **Repository not found**: Ensure repository is in one of the search directories
2. **Worktree already exists**: Script will detect and offer to switch to existing worktree
3. **Branch doesn't exist**: Script will automatically create the branch
4. **Permission issues**: Ensure write access to repository directory

### Debugging

- Use `wt list` to see all current worktrees
- Check the `.worktrees` directory in your repository for physical worktree locations
- Verify repository is in one of the search directories
- Check Git status in the main repository

## Dependencies

- **Git**: Requires Git with worktree support
- **Bash**: Script is written in Bash
- **Standard Unix tools**: Uses common Unix utilities (find, basename, etc.)

## Configuration

The script can be customized by modifying:
- Search directories in `get_search_dirs()` function
- Color schemes in the logging functions
- Default behaviors in command handlers
