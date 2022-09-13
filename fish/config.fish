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

alias kdev-context-authenticate="az aks get-credentials --resource-group ada-dev-rg --name ada-dev-aks02 --admin"
alias kacc-context-authenticate="az aks get-credentials --resource-group ada-acc-rg --name ada-acc-aks02 --admin"
alias kprd-context-authenticate="az aks get-credentials --resource-group ada-prod-rg --name ada-prod-aks02 && kubelogin convert-kubeconfig -l azurecli"

alias kdev-context="kubectx ada-dev-aks02-admin"
alias kacc-context="kubectx ada-acc-aks02-admin"
alias kprd-context="kubectx ada-prod-aks02"
alias kminikube-context="kubectx minikube"

alias kcontext="kubectl config current-context"
alias klogs="kubectl logs -f -n digital"
alias kdashboard="k9s -n digital"

alias ll="lsd -al"
alias ls="pls"
alias tree="lsd --tree"
alias bat="bat --theme=ansi"
alias vim="lvim"
alias vi="lvim"
#alias nvim="lvim"
alias code="vscodium"
alias glances="glances --enable-separator"
alias zellij="zellij -l compact"

alias update="yay -Syu --devel"
alias cleanup="yay -Yc"
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
#: }}}

#: Exports and path {{{
set PATH $PATH /home/simon/bin
set PATH $PATH /home/simon/.local/bin
set PATH $PATH /home/simon/.emacs.d/bin
set PATH $PATH /home/simon/.jenv/bin
set PATH $PATH /home/simon/.yarn/bin
set PATH $PATH /home/simon/.config/yarn/global/node_modules/.bin
set PATH $PATH /home/simon/.cargo/bin

set _Z_SRC /usr/share/z/z.sh
set CM_SELECTIONS clipboard
set TERM kitty
set QT_QPA_PLATFORMTHEME qt5ct
set EDITOR nvim
set SUDO_EDITOR nvim
set KUBE_EDITOR lvim
export SUDO_EDITOR=nvim
#: }}}

#: Sources {{{
source /home/simon/.config/fish/tools/kube.fish

starship init fish | source
#: }}}
