#!/bin/bash
set -euo pipefail

readonly PROJECT_ROOT="$(realpath "$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/../..")"
SESSION_NAME="mlab_mcu_uvm"

function main {
    tmux kill-session -t "$SESSION_NAME" 2>/dev/null || true
    tmux new-session -d -s "$SESSION_NAME"
    tmux source-file "$PROJECT_ROOT/uvm/conf/tmux.config"
    tmux split-window -v -p 50
    tmux split-window -h -p 20
    tmux split-window -v -p 10
    if [ -n "${TMUX:-}" ]; then
        tmux switch-client -t "$SESSION_NAME"
    else
        tmux attach-session -t "$SESSION_NAME"
    fi
}

main
