# Theo's Development Setup Decisions

## Worktree Standardization (Completed)

**Decision**: Centralized worktree location at `~/worktrees/<repo-name>/<branch-name>/`

**Rationale**: 
- Avoids Git weirdness (worktrees outside main repos)
- Predictable location for all worktrees
- Easy to find and manage
- Works with both Crystal worktree managers and VS Code

**Implementation**:
- Created `wt` management script in `~/.dotfiles/bin/wt`
- Migrated existing worktrees from scattered locations
- Configured VS Code to scan `~/worktrees` directory
- Added shell aliases and PATH setup

**Commands**:
```bash
wt create <repo-path> <branch-name>    # Create new worktree
wt list [repo-name]                    # List worktrees
wt remove <repo-name> <branch-name>    # Remove worktree
wt cd <repo-name> <branch-name>        # Switch to worktree
wt clean                               # Clean orphaned worktrees
```

## Current Pain Points Identified

1. **AI Context Fragmentation**: Multiple AI tools (Claude, Cursor, Crystal, Cursor Background Agents) don't share knowledge about preferences and workflow
2. **Documentation Workflow**: Writing docs across different tools (Slab, Google Docs, etc.) - need single interface for copy/edit/paste workflow
3. **Engineering vs Development Time**: Spending too much time engineering tools instead of using them

## Next Steps Planned

1. **Centralized Knowledge Hub**: Capture preferences, workflow patterns, and learnings
2. **AI Context Sharing**: Enable AI tools to reference shared knowledge base
3. **Documentation Workflow**: Single interface for document editing across platforms

## Current Setup

- **Work Organization**: `~/work/elephant/` for job repos, `~/projects/` for personal
- **Terminal**: Warp with zsh
- **Editor**: Helix (primary), Cursor (AI-assisted)
- **AI Tools**: Claude, Ollama, GitHub Copilot
- **Development**: Node.js, Python, Docker, Kubernetes

