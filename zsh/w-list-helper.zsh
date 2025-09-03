#!/usr/bin/env zsh

# Helper function to list available projects
wl() {
    echo "Available projects:"
    local projects_dir="$HOME/work/elephant"
    for dir in $projects_dir/*(N/); do
        if [[ -d "$dir/.git" ]]; then
            echo "  ${dir:t}"
        fi
    done | sort
}

# Helper function to list worktrees for a project
ww() {
    local project="$1"
    if [[ -z "$project" ]]; then
        echo "Usage: ww <project>"
        return 1
    fi
    
    local projects_dir="$HOME/work/elephant"
    local worktrees_dir="$HOME/work/elephant/worktrees"
    
    echo "Worktrees for $project:"
    if [[ -d "$worktrees_dir/$project" ]]; then
        for wt in $worktrees_dir/$project/*(N/); do
            echo "  ${wt:t}"
        done
    else
        echo "  (none)"
    fi
}