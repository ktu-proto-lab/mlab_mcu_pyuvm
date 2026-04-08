#!/bin/bash

readonly PROJECT_ROOT="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/.."

function code_line_metrics {
    cloc --quiet \
        --exclude-dir="__pycache__,sim_build,build,.venv,venv" \
        --match-f='(\.(c|h|v|sv|sh|py|yml)$|^makefile$|^dockerfile$)' "$PROJECT_ROOT" | \
        grep -v "github.com"
}

function project_structure {
    tree "$PROJECT_ROOT"    \
        --dirsfirst         \
        -I '__pycache__|__init__.py|sim_build|build|readme.md|venv' |    \
        sed "1s|^.*$|uvm|"
}

project_structure
code_line_metrics
