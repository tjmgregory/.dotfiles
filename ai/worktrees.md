# WorkTrees: Development Workflow Understanding

## Overview

This system uses Git worktrees to enable parallel development across multiple branches without the overhead of switching branches in a single repository. Worktrees allow you to have multiple working directories for the same repository, each checked out to different branches.

## Core Concept

**Worktrees** are separate working directories that share the same Git repository history. Instead of switching branches in one directory, you can have multiple directories each working on different branches simultaneously.

### Why Use Worktrees?

- **Parallel Development**: Work on multiple features/branches simultaneously
- **No Branch Switching Overhead**: Avoid the time cost of switching branches
- **Clean Separation**: Each branch has its own working directory
- **Easy Context Switching**: Jump between different work contexts instantly

## Our Implementation Strategy

### Storage Location
- **Pattern**: Each repository manages its own worktrees
- **Location**: `<repo-path>/.worktrees/<branch-name>/`
- **Philosophy**: Keep worktrees close to their parent repository

### Management Approach
- **Tool**: Custom `wt` script for standardized management
- **Integration**: Works with VS Code Git Worktree Manager extension
- **Organization**: Repository-specific worktree directories

## Workflow Patterns

### Feature Development
1. **Start**: `wt cd my-repo feature-name` - Creates and switches to feature worktree
2. **Work**: Develop in the dedicated worktree directory
3. **Context Switch**: `wt cd my-repo other-feature` - Switch to different feature
4. **Return**: `wt cd my-repo feature-name` - Return to original feature

### Bug Fixing
1. **Create**: `wt cd my-repo bugfix-123` - Create worktree for bug fix
2. **Fix**: Work on the bug in isolation
3. **Test**: Test the fix without affecting other work
4. **Cleanup**: `wt remove my-repo bugfix-123` - Remove when done

### Code Review
1. **Checkout**: `wt cd my-repo pr-456` - Create worktree for PR branch
2. **Review**: Examine code in dedicated directory
3. **Test**: Run tests or make small changes
4. **Cleanup**: Remove worktree when review is complete

## Mental Model

### Repository Structure
```
my-repo/
├── .git/                    # Main repository
├── .worktrees/             # Worktrees directory
│   ├── feature-auth/       # Feature branch worktree
│   ├── bugfix-123/         # Bug fix worktree
│   └── pr-456/            # PR review worktree
└── ...                     # Main repository files
```

### Development Flow
1. **Main Branch**: Keep main repository on stable branch (main/master)
2. **Feature Work**: All feature development happens in worktrees
3. **Isolation**: Each worktree is completely isolated
4. **Sharing**: All worktrees share the same Git history and can merge/push

## Benefits in Practice

### For AI Agents
- **Clear Context**: Each worktree represents a specific development context
- **Isolated Changes**: Changes in one worktree don't affect others
- **Predictable Structure**: Consistent location pattern across all repositories
- **Easy Navigation**: Simple commands to switch between contexts

### For Development
- **No Stashing**: Never need to stash changes when switching contexts
- **Parallel Work**: Work on multiple features simultaneously
- **Clean History**: Each worktree maintains clean commit history
- **Easy Cleanup**: Remove worktrees when work is complete

## Integration Points

### VS Code
- **Extension**: Git Worktree Manager automatically discovers worktrees
- **Workspace**: Each worktree can be opened as separate VS Code workspace
- **IntelliSense**: Full language support in each worktree

### Terminal/Shell
- **Navigation**: `wt cd` commands for quick directory switching
- **Listing**: `wt list` to see all active worktrees
- **Management**: `wt remove` and `wt clean` for maintenance

## Best Practices

### Naming Conventions
- **Features**: `feature-auth`, `feature-payments`
- **Bug Fixes**: `bugfix-123`, `fix-login-issue`
- **PRs**: `pr-456`, `review-auth-changes`
- **Experiments**: `experiment-new-ui`, `spike-performance`

### Workflow Discipline
1. **One Purpose**: Each worktree should have a single, clear purpose
2. **Regular Cleanup**: Remove worktrees when work is complete
3. **Consistent Naming**: Use descriptive, consistent branch names
4. **Main Branch**: Keep main repository on stable branch

### AI Agent Guidelines
- **Context Awareness**: Always check which worktree you're working in
- **Isolation Respect**: Changes in one worktree don't affect others
- **Cleanup**: Suggest removing worktrees when work is complete
- **Navigation**: Use `wt` commands for worktree management

## Common Scenarios

### Starting New Feature
```bash
# Create and switch to new feature worktree
wt cd my-repo feature-user-dashboard

# Work in the new directory
# All changes are isolated to this worktree
```

### Switching Between Features
```bash
# Switch to different feature
wt cd my-repo feature-payments

# Previous worktree remains unchanged
# Can switch back anytime
```

### Code Review Workflow
```bash
# Create worktree for PR review
wt cd my-repo pr-789

# Review code, run tests, make suggestions
# All isolated from other work

# Clean up when done
wt remove my-repo pr-789
```

## Troubleshooting Mental Models

### "Where am I?"
- Use `pwd` to see current directory
- Use `wt list` to see all worktrees
- Check if you're in a `.worktrees` directory

### "Why can't I see my changes?"
- Verify you're in the correct worktree
- Check if you're in the main repository vs worktree
- Use `git status` to see current branch

### "How do I get back to main?"
- `wt cd my-repo main` - Switch to main branch worktree
- Or navigate to main repository directory directly

## Reference

For detailed implementation and command reference, see [`../bin/wt.md`](../bin/wt.md).