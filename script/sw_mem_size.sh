#!/bin/bash
set -e

# TODO: support on xcelium

readonly SCRIPT_SW_MEM_SIZE_ERROR_PROJECT_ROOT_NOT_DEFINED=997
readonly SCRIPT_SW_MEM_SIZE_ERROR_MCU_TEST_SW_DIR_NOT_DEFINED=998
readonly SCRIPT_SW_MEM_SIZE_ERROR_MCU_TEST_NAME_NOT_DEFINED=999
readonly SCRIPT_SW_MEM_SIZE_ERROR_MCU_TEST_ENV_SW_MEM_SIZE_FILEPATH_NOT_DEFINED=1000
readonly SCRIPT_SW_MEM_SIZE_ERROR_SUPPORTED_COMPILER_NOT_FOUND=1001

if [ -z ${PROJECT_ROOT+x} ]; then
    exit $SCRIPT_ERROR_SW_MEM_SIZE_PROJECT_ROOT_NOT_DEFINED
fi

if [ -z ${MCU_TEST_SW_DIR+x} ]; then
    exit $SCRIPT_SW_MEM_SIZE_ERROR_MCU_TEST_SW_DIR_NOT_DEFINED
fi

if [ -z ${MCU_TEST_NAME+x} ]; then
    exit $SCRIPT_SW_MEM_SIZE_ERROR_MCU_TEST_NAME_NOT_DEFINED
fi

if [ -z ${MCU_TEST_ENV_SW_MEM_SIZE_FILEPATH+x} ]; then
    exit $SCRIPT_SW_MEM_SIZE_ERROR_MCU_TEST_ENV_SW_MEM_SIZE_FILEPATH_NOT_DEFINED
fi

source "$PROJECT_ROOT/uvm/script/logger.sh"

if command -v riscv64-unknown-elf-size &> /dev/null; then
    riscv64-unknown-elf-size -A "$MCU_TEST_SW_DIR/$MCU_TEST_NAME.elf" | head -n 9 > "$MCU_TEST_ENV_SW_MEM_SIZE_FILEPATH"

elif command -v riscv64-linux-gnu-size &> /dev/null; then
    riscv64-linux-gnu-size -A  "$MCU_TEST_SW_DIR/$MCU_TEST_NAME.elf" | head -n 9 > "$MCU_TEST_ENV_SW_MEM_SIZE_FILEPATH"

else
    logger ERROR "can not extract size of the compiled elf file"
    exit SCRIPT_SW_MEM_SIZE_ERROR_SUPPORTED_COMPILER_NOT_FOUND
fi

printf "\nfrom: script/sw_mem_size\n" >> "$MCU_TEST_ENV_SW_MEM_SIZE_FILEPATH"
