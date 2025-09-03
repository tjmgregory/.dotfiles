export EDITOR='hx'
export VISUAL='hx'

alias h='hx'
alias g='lazygit'
alias y='yarn'
alias n='npm'
alias v='vim'
alias p='pnpm'
alias d='deno'
alias dt='d task'

alias cat='bat'

# Git
alias gl='git pull'
alias gp='git push'
alias gco='git checkout'
alias gst='git status'
alias gd='git diff'

# Edit commands in vim with v in normal mode
autoload edit-command-line; zle -N edit-command-line
bindkey -M vicmd v edit-command-line

# Useful scripts
alias formatjson='pbpaste | python3 -m json.tool | pbcopy'
alias isodate='date -u +"%Y-%m-%dT%H:%M:%SZ" | tr -d '\n' | tee >(pbcopy)'
alias ll='ls -la'
alias text="pbpaste | pbcopy"
alias uuid='python3 -c "import uuid; import sys; sys.stdout.write(\"{}\".format(uuid.uuid4()))" | tee >(pbcopy)'
function sha1 { echo -n "$1" | openssl sha1 | tee >(pbcopy) }

# React testing library print limit
export DEBUG_PRINT_LIMIT=100000000

alias k='kubectl'
[[ "$TERM_PROGRAM" == "vscode" ]] && source <(kubectl completion zsh)

# helix-gpt https://github.com/leona/helix-gpt
export HANDLER=copilot

# Kraft Cloud
export UKC_METRO=fra0


# Worktree management
export PATH="$HOME/.dotfiles/bin:$PATH"

# Shell function wrapper for wt that handles cd properly
unalias wt 2>/dev/null  # Remove any existing alias
wt() {
    if [[ "$1" == "cd" ]]; then
        # Handle cd command specially to actually change directory
        local target_dir
        target_dir=$(~/.dotfiles/bin/wt cd "$2" "$3" --print-path 2>/dev/null)
        
        if [[ $? -eq 0 && -n "$target_dir" && -d "$target_dir" ]]; then
            cd "$target_dir"
            echo "Switched to worktree: $target_dir"
        else
            # Fallback to regular wt cd behavior (will show output but not change dir)
            ~/.dotfiles/bin/wt cd "$2" "$3"
        fi
    else
        # For all other commands, just pass through to the script
        ~/.dotfiles/bin/wt "$@"
    fi
}
