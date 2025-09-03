#!/bin/bash

# Auto-branch script for VSCode Extension @ext:jackiotyu.git-worktree-manager
# Creates a new branch with the worktree name automaticallyif current branch is "main"

# Get the worktree directory name from the current directory
# This works whether we're in a .worktrees subdirectory or using the extension's $WORKTREE_PATH
if [ -n "$WORKTREE_PATH" ]; then
    # If $WORKTREE_PATH is provided by the extension, use it
    WORKTREE_NAME=$(basename "$WORKTREE_PATH")
else
    # Otherwise, get the current directory name
    WORKTREE_NAME=$(basename "$PWD")
fi

# Get the current branch name
CURRENT_BRANCH=$(git branch --show-current)

# Check if current branch is "main"
if [ "$CURRENT_BRANCH" = "main" ]; then
    echo "Current branch is 'main', creating new branch: $WORKTREE_NAME"
    
    # Create and checkout the new branch
    git checkout -b "$WORKTREE_NAME"
    
    if [ $? -eq 0 ]; then
        echo "Successfully created and switched to branch: $WORKTREE_NAME"
    else
        echo "Failed to create branch: $WORKTREE_NAME"
        exit 1
    fi
else
    echo "Current branch is '$CURRENT_BRANCH', staying on current branch"
fi
