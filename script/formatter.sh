#!/usr/bin/env bash

set -euo pipefail -c

readonly FORMATTER_PROJECT_ROOT="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/../.."

source "$FORMATTER_PROJECT_ROOT/uvm/script/logger.sh"

logger INFO "formatting started"

ruff format .
ruff check . --fix
logger INFO "python"

find . -name '*.c' -o -name '*.h' | xargs clang-format -i
logger INFO "c"

shfmt -w .
logger INFO "bash"

find . -name '*.sv' | xargs verible-verilog-format --inplace
logger INFO "systemverilog"

logger SUCCESS "formatting done"