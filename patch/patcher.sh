#!/bin/bash

readonly CALL_PATH="$(pwd)"
readonly PROJECT_ROOT="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/../.."

readonly OPT_APPLY_PATCHES="--apply"
readonly OPT_REVERSE_PATCHES="--reverse"

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
    $OPT_APPLY_PATCHES:     apply patches
    $OPT_REVERSE_PATCHES:   restore patches (return to untouched state)

EOF
    exit 1
fi

if ! command -v patch >/dev/null 2>&1; then
    echo "[  ERROR]: 'patch' utility is not installed"
    echo "            can be installed with:"
    echo "            sudo at install patch"
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
    # EEPROM compatibility with cocotb (to work on Verilator)
    apply_patch ./tb/misc/24CS512.sv  ./uvm/patch/eeprom.patch

    # Avoiding relative paths to RTL source files (to work on XCelium)
    apply_patch ./sim/rtl/files.f     ./uvm/patch/rtl_files.patch

    echo "[   INFO]: Patches applied"

elif $REVERSE_PATCHES; then
    reverse_patch ./tb/misc/24CS512.sv  ./uvm/patch/eeprom.patch
    reverse_patch ./sim/rtl/files.f     ./uvm/patch/rtl_files.patch
    echo "[   INFO]: Returned to previous state"
fi

cd "$CALL_PATH"