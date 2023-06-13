# vim:fileencoding=utf-8:ft=fish:foldmethod=marker
#: Configuration {{{
#suppress welcome message
set fish_greeting

# fix for lsd not using correct colours
ls > /dev/null
#: }}}

#: Aliases {{{
alias helm_2.13.1="docker run -it --rm -v ~/.kube/config:/root/.kube/config -v ~/.helm:/root/.helm alpine/helm:2.13.1"
alias helm_2.15.2="docker run -it --rm -v ~/.kube/config:/root/.kube/config -v ~/.helm:/root/.helm alpine/helm:2.15.2"
alias helm_2.17.0="docker run -it --rm -v ~/.kube/config:/root/.kube/config -v ~/.helm:/root/.helm alpine/helm:2.17.0"

alias kdev-context-authenticate="az aks get-credentials --resource-group ada-dev-rg --name ada-aks-dev --admin"
alias kacc-context-authenticate="az aks get-credentials --resource-group ada-acc-rg --name ada-aks-acc --admin"
alias kprd-context-authenticate="az aks get-credentials --resource-group ada-prod-rg --name ada-aks-prod && kubelogin convert-kubeconfig -l azurecli"

alias kdev-context="kubectx ada-aks-dev-admin"
alias kacc-context="kubectx ada-aks-acc-admin"
alias kprd-context="kubectx ada-aks-prod"
alias kminikube-context="kubectx minikube"

alias kcontext="kubectl config current-context"
alias klogs="kubectl logs -f -n digital"
alias kdashboard="k9s -n digital"
alias kdash="k9s -n digital"

alias ll="exa --long --all --icons"
alias ls="exa --long --icons"
alias tree="exa --tree --icons"
alias bat="bat --theme=Catppuccin-mocha"
alias cat="bat -p --theme=Catppuccin-mocha"
alias vim="nvim"
alias code="vscodium"
alias glances="glances --enable-separator"
alias tmx="TERM=xterm-256color tmux"
alias tms="tmux-sessionizer"

alias update="yay -Syu --devel"
alias cleanup="yay -Yc"
#: }}}

#: Keybinds {{{
bind \cf 'tmux-sessionizer'
bind \cr 'searchHistory'
#: }}}

#: Functions {{{
function sudo
	if test "$argv" = !!
	   	eval command sudo $history[1]
	else
		command sudo $argv
	end
end

function base64Decode --description "Decode base64 input"
  command echo $argv | base64 --decode
end

function base64Encode --description "Encode input to base64"
  command echo $argv | base64 
end

function sd --description "Search directories"
  if test -z "$argv"
    eval cd ~ && cd $(fd -H -t directory | fzf)
  else
    eval cd $argv && cd $(fd -H -t directory | fzf)
  end
end

function searchHistory --description "Search command history"
 commandline $(history | fzf)
end

function searchDirectory
    eval cd $(fd -H -t directory | fzf)
end
#: }}}

#: Exports and path {{{
set PATH $PATH /home/simon/bin
set PATH $PATH /home/simon/.local/bin
set PATH $PATH /home/simon/.emacs.d/bin
set PATH $PATH /home/simon/.jenv/bin
set PATH $PATH /home/simon/.yarn/bin
set PATH $PATH /home/simon/.config/yarn/global/node_modules/.bin
set PATH $PATH /home/simon/.cargo/bin
set PATH $PATH /home/simon/.config/lsp/lua-language-server/bin
set PATH $PATH /usr/local/go/bin
set PATH $PATH /home/simon/.config/emacs/bin

set FZF_DEFAULT_OPTS --color=bg:-1,bg+:#302d41,hl+:#ddb6f2,hl:#ddb6f2,pointer:#ddb6f2

set _Z_SRC /usr/share/z/z.sh
set CM_SELECTIONS clipboard
set TERM kitty
set QT_QPA_PLATFORMTHEME qt5ct
set EDITOR nvim
set SUDO_EDITOR nvim
set KUBE_EDITOR nvim
set BAT_THEME Catppuccin-mocha
export SUDO_EDITOR=nvim
#: }}}

#: Sources {{{
source /home/simon/.config/fish/tools/kube.fish
function starship_transient_rprompt_func
  starship module time
end
starship init fish | source
enable_transience
#: }}}

set -q GHCUP_INSTALL_BASE_PREFIX[1]; or set GHCUP_INSTALL_BASE_PREFIX $HOME ; set -gx PATH $HOME/.cabal/bin $PATH /home/simon/.ghcup/bin # ghcup-env
