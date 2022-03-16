# Fish implementation of https://github.com/kubermatic/fubectl

alias _kctl_tty="kubectl"
alias _inline_fzf="fzf --multi --ansi -i -1 --height=50% --reverse -0 --header-lines=1 --inline-info --border"
alias _inline_fzf_nh="fzf --multi --ansi -i -1 --height=50% --reverse -0 --inline-info --border"
alias _kforward="kubectl port-forward -n"

function _isClusterSpaceObject
  set obj $argv
  kubectl api-resources --namespaced=false \
    | awk '(apiidx){print substr($0, 0, apiidx),substr($0, kindidx) } (!apiidx){ apiidx=index($0, " APIVERSION");kindidx=index($0, " KIND")}' \
    | grep -iq "\<$obj\>"
end

function kdes --argument kind --description "Describe kubernetes resource, 'kind' parameter defaults to pod"
  set -q kind[1]; or set kind "pod"
  if _isClusterSpaceObject $kind
    kubectl get "$kind" | _inline_fzf | awk '{print $1}' | xargs -r kubectl describe "$kind"
  else
    kubectl get "$kind" --all-namespaces | _inline_fzf | awk '{print $1, $2}' | string split -n " " | xargs -r kubectl describe "$kind" -n
  end
end

function kget --argument kind --description "Get kubernetes resource, 'kind' parameter defaults to pod"
  set -q kind[1]; or set kind "pod"
  if _isClusterSpaceObject $kind
    kubectl get "$kind" | _inline_fzf | awk '{print $1}' | xargs -r kubectl describe "$kind"
  else
    kubectl get "$kind" --all-namespaces | _inline_fzf | awk '{print $1, $2}' | string split -n " " | xargs -r kubectl get "$kind" -o yaml -n
  end
end

function kfor --description "Port forward a container port from cluster, usage: kfor LOCAL_PORT:CONTAINER_PORT" 
  set port $argv
  [ -z "$port" ] && printf "kfor: missing argument.\nUsage: kfor LOCAL_PORT:CONTAINER_PORT\n" && return 255
  set arg_pair (kubectl get po --all-namespaces | _inline_fzf | awk '{print $1, $2}' | string split -n " ")
  [ -z "$arg_pair" ] && printf "kfor: no pods found. no forwarding.\n" && return
  _kctl_tty port-forward -n $arg_pair $port
end

function kex --argument cmd --description "Execute command in container, usage kex CMD [ARGS]"
  [ -z "$cmd" ] && printf "kex: missing argument(s)." && return 255 
  set arg_pair (kubectl get po --all-namespaces | _inline_fzf | awk '{print $1, $2}' | string split -n " ")
  [ -z "$arg_pair" ] && printf "kex: no pods found. no execution.\n" && return 255
  set containers_out (echo "$arg_pair" | xargs kubectl get po -o=jsonpath='{.spec.containers[*].name}' -n)
  set container_choosen (echo "$containers_out" |  tr ' ' "\n" | _inline_fzf_nh)
  _kctl_tty exec -it -n $arg_pair -c $container_choosen -- $cmd
end

function kwns --description "Watch pods in a namespace"
  set ns (kubectl get ns | _inline_fzf | awk '{print $1}')
  [ -z "$ns" ] && printf "kcns: no namespace selected/found.\n" && return
  watch kubectl get pod -n $ns
end
