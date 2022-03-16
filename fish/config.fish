# suppress welcome message
set fish_greeting

# fix for lsd not using correct colours
ls > /dev/null

# Aliases
alias helm_2.13.1="docker run -it --rm -v ~/.kube/config:/root/.kube/config -v ~/.helm:/root/.helm alpine/helm:2.13.1"
alias helm_2.15.2="docker run -it --rm -v ~/.kube/config:/root/.kube/config -v ~/.helm:/root/.helm alpine/helm:2.15.2"
alias helm_2.17.0="docker run -it --rm -v ~/.kube/config:/root/.kube/config -v ~/.helm:/root/.helm alpine/helm:2.17.0"

alias kdev-context="az aks get-credentials --resource-group ada-dev-rg --name ada-dev-aks02 --admin"
alias kacc-context="az aks get-credentials --resource-group ada-acc-rg --name ada-acc-aks02 --admin"
alias kprod-context="az aks get-credentials --resource-group ada-prod-rg --name ada-prod-aks02"

alias kcontext="kubectl config current-context"
alias kproxy="kubectl proxy --port 8002"
alias klogs="kubectl logs -f -n digital"
alias kdashboard="k9s -n digital"

alias ll="lsd -al"
alias tree="lsd --tree"
alias bat="bat --theme=Dracula"
alias vim="lvim"
alias vi="lvim"
alias code="vscodium"

alias update="yay -Syu --devel"
alias cleanup="yay -Yc"

# Functions
function kdebug --description="Start kubernetes debug pod"
	if [ -n "$argv" ]
		kubectl run debug --rm -i --tty --image "$argv" -n digital --generator=run-pod/v1
	else
		kubectl run debug --rm -i --tty --image radial/busyboxplus:curl -n digital --generator=run-pod/v1
	end
end

function ktail --description="Use kubetail to follow app logging"
	kubetail -n digital -l app="$argv"
end

function kport --description="Start kubernetes port forward"
	kubectl port-forward -n digital deployment/"$argv[1]" "$argv[2]":8080
end

function kcleanup --description="Cleanup evicted pods"
	kubectl get po -n digital -o json | \
	jq  '.items[] | select(.status.reason!=null) | select(.status.reason | contains("Evicted")) | 
	"kubectl delete po \(.metadata.name) -n \(.metadata.namespace)"' | xargs -n 1 bash -c
end

function kwatch --description="Watch kubernetes pods"
	if [ -n "$argv" ]
		watch "kubectl -n digital get pods| grep '$argv'"
	else
		watch "kubectl -n digital get pods"
	end
end

function ktop
	if [ -n "$argv" ]
		watch "kubectl -n digital top pods | grep '$argv'"
	else
		watch "kubectl -n digital top pods"
	end
end

function sudo
	if test "$argv" = !!
	   	eval command sudo $history[1]
	else
		command sudo $argv
	end
end

# Exports
set PATH $PATH /home/simon/bin
set PATH $PATH /home/simon/.local/bin
set PATH $PATH /home/simon/.emacs.d/bin
set PATH $PATH /home/simon/.jenv/bin
set PATH $PATH /home/simon/.yarn/bin
set PATH $PATH /home/simon/.config/yarn/global/node_modules/.bin

set _Z_SRC /usr/share/z/z.sh
set CM_SELECTIONS clipboard
set TERM kitty
set QT_QPA_PLATFORMTHEME gtk2
set EDITOR nvim
set SUDO_EDITOR nvim
export SUDO_EDITOR=nvim

source /home/simon/.config/fish/tools/fubectl.fish

starship init fish | source
