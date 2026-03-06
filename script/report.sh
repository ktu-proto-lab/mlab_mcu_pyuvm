#!/bin/bash

readonly PROJECT_ROOT="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/.."

function code_line_metrics {
    cloc --quiet                                                            \
        --match-f='(\.(c|h|v|sv|sh|py)$|^makefile$)' "$PROJECT_ROOT" |      \
        grep -v "github.com"
}

function project_structure {
    tree "$PROJECT_ROOT"    \
        --dirsfirst         \
        -I '__pycache__'    \
        -I '__init__.py'    \
        -I 'readme.md' |    \
        sed "1s|^.*$|uvm|"
}

project_structure
code_line_metrics
