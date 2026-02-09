#!/bin/bash

readonly CALL_PATH="$(pwd)"
readonly PROJECT_ROOT="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/../.."

OPT_APPLY_PATCHES="--apply"
OPT_RESTORE_PATCHES="--restore"

APPLY_PATCHES=false
RESTORE_PATCHES=false

while [ $# -gt 0 ]; do
    case $1 in
    "$OPT_APPLY_PATCHES")
        APPLY_PATCHES=true
        ;;
    "$OPT_RESTORE_PATCHES")
        RESTORE_PATCHES=true
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
    patch ./tb/misc/24CS512.sv < ./uvm/patch/eeprom.patch

elif $RESTORE_PATCHES; then
    patch -R ./tb/misc/24CS512.sv < ./uvm/patch/eeprom.patch
fi

cd "$CALL_PATH"