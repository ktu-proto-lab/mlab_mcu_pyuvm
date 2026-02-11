#!/bin/bash

readonly CALL_PATH="$(pwd)"
readonly PROJECT_ROOT="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/../.."

readonly OPT_APPLY_PATCHES="--apply"
readonly OPT_REVERSE_PATCHES="--reverse"

if [[ $# -eq 0 ]]; then
    cat <<EOF
Usage:
    ./patcher.sh [options]

Options:
    $OPT_APPLY_PATCHES:     apply patches
    $OPT_REVERSE_PATCHES:   restore patches (return to untouched state)

EOF
    exit 1
fi

APPLY_PATCHES=false
REVERSE_PATCHES=false

while [ $# -gt 0 ]; do
    case $1 in
    "$OPT_APPLY_PATCHES")
        APPLY_PATCHES=true
        ;;
    "$OPT_REVERSE_PATCHES")
        REVERSE_PATCHES=true
        ;;
    -*)
      echo "[  ERROR]: Unknown provided option $1"
      exit 1
      ;;
    esac
    shift
done

cd "$PROJECT_ROOT"

if $APPLY_PATCHES; then
    # EEPROM compatibility with cocotb
    patch -Nfs -V none -r - ./tb/misc/24CS512.sv < ./uvm/patch/eeprom.patch
    echo "[   INFO]: Patches applied"

elif $REVERSE_PATCHES; then
    patch -Rfs -V none -r - ./tb/misc/24CS512.sv < ./uvm/patch/eeprom.patch
    echo "[   INFO]: Returned to previous state"
fi

cd "$CALL_PATH"