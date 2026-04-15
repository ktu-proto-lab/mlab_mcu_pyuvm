#!/bin/bash
set -euo pipefail

readonly PROJECT_ROOT="$(realpath "$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/../..")"
SESSION_NAME="mlab_mcu_uvm_env"

function main {
    tmux kill-session -t "$SESSION_NAME" 2>/dev/null || true

    # Configure pane layout
    SIM_PANE=$(tmux new-session -d -P -F "#{pane_id}" -s "$SESSION_NAME" -e "PROJECT_ROOT=$PROJECT_ROOT")
    TERMINAL_PANE=$(tmux split-window -v -p 20 -P -F "#{pane_id}")
    TRACER_PANE=$(tmux split-window -h -p 10 -P -F "#{pane_id}")

    # Allow to use mouse and provide quick session kill key bind
    tmux source-file "$PROJECT_ROOT/uvm/conf/tmux.conf"

    # Give names at the top of panes to express intent
    tmux set-option -t "$SESSION_NAME" pane-border-status top
    tmux set-option -p -t "$SIM_PANE" @pane_title "sim"
    tmux set-option -p -t "$TRACER_PANE" @pane_title "tracer"
    tmux set-option -p -t "$TERMINAL_PANE" @pane_title "terminal"

    tmux select-pane -t "$TERMINAL_PANE"

    # Start session
    if [ -n "${TMUX:-}" ]; then
        # if by mistake user is inside the other tmux session
        tmux switch-client -t "$SESSION_NAME"
    else
        tmux attach-session -t "$SESSION_NAME"
    fi
}

# TODO:
# if none args provided, inform to use help
# if help is provided, show usage of the script
# if init is provided initialize tmux session
main
