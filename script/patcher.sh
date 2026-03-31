#!/bin/bash

readonly PATCHER_CALL_PATH="$(pwd)"
readonly PATCHER_PROJECT_ROOT="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/../.."

readonly PATCHER_OPT_APPLY_PATCHES="--apply"
readonly PATCHER_OPT_REVERSE_PATCHES="--reverse"

source "$PATCHER_PROJECT_ROOT/uvm/script/logger.sh"

function apply_patch {
    # >/dev/null    - suppress stdout
    # >&1           - suppress stderr
    # || true       - ignore non-zero exit status (script does not fail)
    patch -Nfs -V none -r - "$1" < "$2" >/dev/null 2>&1 || true
}

function reverse_patch {
    patch -Rfs -V none -r - "$1" < "$2" >/dev/null 2>&1 || true
}

if [[ $# -eq 0 ]]; then
    cat <<EOF
Usage:
    ./patcher.sh [options]

Options:
    $PATCHER_OPT_APPLY_PATCHES:     apply patches
    $PATCHER_OPT_REVERSE_PATCHES:   restore patches (return to untouched state)

EOF
    exit 1
fi

if ! command -v patch >/dev/null 2>&1; then
    logger ERROR "'patch' utility is not installed"
    echo "            can be installed with:"
    echo "            sudo at install patch"
    exit 1
fi

PATCHER_APPLY_PATCHES=false
PATCHER_REVERSE_PATCHES=false

while [ $# -gt 0 ]; do
    case $1 in
    "$PATCHER_OPT_APPLY_PATCHES")
        PATCHER_APPLY_PATCHES=true
        ;;
    "$PATCHER_OPT_REVERSE_PATCHES")
        PATCHER_REVERSE_PATCHES=true
        ;;
    -*)
      logger ERROR "unknown provided option $1"
      exit 1
      ;;
    esac
    shift
done

cd "$PATCHER_PROJECT_ROOT"

if $PATCHER_APPLY_PATCHES; then
    # EEPROM compatibility with cocotb (to work on Verilator)
    apply_patch ./tb/misc/24CS512.sv  ./uvm/patch/eeprom.patch

    # Avoiding relative paths to RTL source files (to work on XCelium)
    apply_patch ./sim/rtl/files.f     ./uvm/patch/rtl_files.patch

    logger INFO "patches applied"

elif $PATCHER_REVERSE_PATCHES; then
    reverse_patch ./tb/misc/24CS512.sv  ./uvm/patch/eeprom.patch
    reverse_patch ./sim/rtl/files.f     ./uvm/patch/rtl_files.patch
    logger INFO "returned to previous state"
fi

cd "$PATCHER_CALL_PATH"
