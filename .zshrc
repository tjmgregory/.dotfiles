# Custom function dirs go on fpath BEFORE compinit
fpath+=~/.zfunc

# compinit: full run only once per day; otherwise use cached dump.
# Saves ~70-100ms vs running full compinit on every shell.
# https://stackoverflow.com/a/74323525 - stops compdef message on new session
autoload -Uz compinit
if [[ -n ~/.zcompdump(#qNmh-24) ]]; then
  compinit -C
else
  compinit
fi

source ~/.dotfiles/.zshrc.aliases
source ~/.dotfiles/.zshrc.elephant
source ~/.dotfiles/.zshrc.secret

# Lazy-load nvm — saves ~400ms on every shell startup.
# nvm/node/npm/npx stubs source nvm.sh on first invocation, then re-call themselves.
export NVM_DIR="$HOME/.nvm"
_nvm_lazy_load() {
  unset -f nvm node npm npx 2>/dev/null
  [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
  [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
}
nvm()  { _nvm_lazy_load; nvm "$@"; }
node() { _nvm_lazy_load; node "$@"; }
npm()  { _nvm_lazy_load; npm "$@"; }
npx()  { _nvm_lazy_load; npx "$@"; }

# Force reload completions for w function in Warp
if [[ "$TERM_PROGRAM" == "WarpTerminal" ]]; then
  autoload -U +X _w
fi
bindkey '^I' complete-word

# Created by `pipx` on 2025-08-16 08:30:41
export PATH="$PATH:/Users/theo/.local/bin"

# bun completions
[ -s "/Users/theo/.bun/_bun" ] && source "/Users/theo/.bun/_bun"

# bun
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"

# antidote — hardcoded brew prefix to skip the ~20ms `brew --prefix` fork
source /opt/homebrew/opt/antidote/share/antidote/antidote.zsh
# initialize plugins statically with ${ZDOTDIR:-~}/.zsh_plugins.txt
antidote load

# Starship - must be at the end
eval "$(starship init zsh)"


# Android
export JAVA_HOME=$HOMEBREW_PREFIX/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$HOME/Library/Android/sdk/platform-tools

# go
export PATH=$PATH:/Users/theo/go/bin

# User bin directory (after bun so ~/bin/qmd shadows ~/.bun/bin/qmd)
export PATH="$HOME/bin:$PATH"

zstyle ':completion:*' menu select

# Vim terminal
# set -o vi

# omnara
export OMNARA_INSTALL="$HOME/.omnara"
export PATH="$OMNARA_INSTALL/bin:$PATH"

source /Users/theo/.zsh_kraft_completion;
