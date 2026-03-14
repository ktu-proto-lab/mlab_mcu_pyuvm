#!/bin/bash
set -euo pipefail

# TODO: add simulator configuration support
readonly INIT_CALL_PATH="$(pwd)"
readonly INIT_PROJECT_ROOT="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/.."

readonly INIT_ARG_COUNT=$#
readonly INIT_OPT_HELP="--help"
readonly INIT_OPT_DOCKER="--docker"
readonly INIT_OPT_ENV="--env"
readonly INIT_OPT_RUN_SANITY_TEST="--test"

source "$INIT_PROJECT_ROOT/script/logger.sh"

function init_docker {
    if ! docker info >/dev/null 2>&1; then
        logger WARNING "docker requires sudo or user lacks permissions"

        if ! groups | grep -q docker; then
            logger INFO "adding user '$USER' to docker group..."
            sudo usermod -aG docker "$USER"

            logger INFO "please log out and log back in, reboot, or run: 'newgrp docker'"
        fi

        exit 1
    fi
    cd "$INIT_PROJECT_ROOT"
    logger INFO "building docker image"
    docker compose build
    logger INFO "running docker container"
    docker compose run --rm uvm \
        bash -c "source /home/mcu/uvm/script/logger.sh && logger SUCCESS 'you are now inside built container'; exec bash"
}

function init_env {
    logger INFO "initializing python virtual environment"
    python3 -m venv "$INIT_PROJECT_ROOT/.venv"
    source "$INIT_PROJECT_ROOT/.venv/bin/activate"
    pip install --upgrade pip
    pip install -r "$INIT_PROJECT_ROOT/conf/requirements.txt"
    source "$INIT_PROJECT_ROOT/script/patcher.sh" --apply
    logger SUCCESS "environment initialized"
}

function run_sanity_test {
    logger INFO "building dut's behavioral firmware"
    cd "$INIT_PROJECT_ROOT/sw/test/gpio/mirror"
    make clean && make
    cd "$INIT_PROJECT_ROOT/sim"
    source "$INIT_PROJECT_ROOT/.venv/bin/activate"
    logger INFO "running simulation"
    make clean && make
}

function print_help {
    cat <<EOF
Initialize project's work environment script

Usage:
    $(basename "$0") [options]

Options:
    $INIT_OPT_DOCKER:           Docker Container (otherwise use script/setup.sh)
    $INIT_OPT_ENV:              Python's Virtual Environment and Patching
    $INIT_OPT_RUN_SANITY_TEST:             Run GPIO's Mirror Test

Simulator:
    Yet to be added as of 07.03.26
EOF
}
########################################################################################################################
### Main
########################################################################################################################
if [[ $# -eq 0 ]]; then
    print_help
    exit 1
fi

INIT_PRINT_HELP=false
INIT_DOCKER=false
INIT_ENV=false
INIT_RUN_SANITY_TEST=false
while [[ $# -gt 0 ]]; do
    case "$1" in
    "$INIT_OPT_HELP")
        INIT_PRINT_HELP=true
        ;;
    "$INIT_OPT_DOCKER")
        INIT_DOCKER=true
        ;;
    "$INIT_OPT_ENV")
        INIT_ENV=true
        ;;
    "$INIT_OPT_RUN_SANITY_TEST")
        INIT_RUN_SANITY_TEST=true
        ;;
    -*)
        logger ERROR "unknown provided option '$1'"
        exit 1
        ;;
    *)
        logger ERROR "script does not take non-option arguments '$1'"
        exit 1
        ;;
    esac
    shift
done

if $INIT_PRINT_HELP; then
    print_help
    exit
fi

cd "$INIT_PROJECT_ROOT"

if [[ $INIT_DOCKER == true && $INIT_ARG_COUNT -gt 1 ]]; then
    logger ERROR "select $INIT_OPT_DOCKER, then run script in the container to finish project initialization"
    exit 1
fi

if [[ $INIT_DOCKER == true ]]; then
    if [[ -f /.dockerenv ]]; then
        logger ERROR "refusing to create new container while being inside docker's container, exit to create one"
        exit 1
    fi
    init_docker
fi

if [[ $INIT_ENV == true ]]; then
    init_env
fi

if [[ $INIT_RUN_SANITY_TEST == true ]]; then
    run_sanity_test
fi

cd "$INIT_CALL_PATH"
