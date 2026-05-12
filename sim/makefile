SHELL := /bin/bash
.SHELLFLAGS := -euo pipefail -c

PROJECT_ROOT = $(abspath ../..)
export PROJECT_ROOT

# TODO: clean recipie for both xcelium and verilator (remove waveform files, results)

# ----------------------------------------------------------------------------------------------------------------------
# Options
# ----------------------------------------------------------------------------------------------------------------------
SIM ?=

# pyuvm tests
TEST ?=

# cocotb testbenches
TB ?=

# Do not generate waveform files by default for better performance
WAVES ?= 0

# SimVision GUI
GUI ?= 0

# Log level of testbenches and tests
LOG ?= INFO

# test software running on dut
SW ?=

# test coverage reporting from simulator
COV ?= 0

CLEAN_RUN ?= 0

TRACER_LINE_COUNT ?= 30

define HELP_USAGE
------------------------------------------------------------------------------------------------------------------------
Usage:
  make [SIM=...] [TEST=... | TB=...] [WAVES=1] [GUI=1] [LOG=...]

Simulators:
  SIM=verilator     : run on Verilator
  SIM=xcelium       : run on Cadence Xcelium

Test:
  TEST=test_name    : run a pyuvm test with software from 'sw/test'
  TB=tb_name        : run a cocotb testbench with software from 'sw/tb'
  SW=dir_name       : override software directory

Options:
  WAVES=1                       : capture waves in waveform 'dump.vcd' file
  GUI=1                         : open SimVision GUI (only when SIM=xcelium)
  LOG=debug|info|warning|error  : set logging level (default: info)

Requirements:
  1. TEST or TB must be defined.
  2. Software directory must contain a 'main.c' file.

Test transaction tracer:
  make tracer [TRACER_LINE_COUNT=n]

Examples:
  make TEST=simple_gpio_test WAVES=1
  make SIM=xcelium TB=uart_tb GUI=1
  make TEST=uart_simple_test LOG=debug
  make tracer
  make tracer TRACER_LINE_COUNT=50
------------------------------------------------------------------------------------------------------------------------
endef
export HELP_USAGE

.PHONY: help
help:
	@echo "$$HELP_USAGE"; \
	exit

.DEFAULT_GOAL := all

# ----------------------------------------------------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------------------------------------------------
TOPLEVEL_LANG = verilog

TOPLEVEL = mcu

# ----------------------------------------------------------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------------------------------------------------------
# Cocotb discovers Python testbench modules via PYTHONPATH
export PYTHONPATH := $(PROJECT_ROOT)/uvm/tb:$(PYTHONPATH)

ifeq ($(TB),)
	MODULE = test.$(TEST)

	ifeq ($(SW),)
		SW_DIR = $(PROJECT_ROOT)/uvm/sw/test/$(TEST)
	else
		SW_DIR = $(PROJECT_ROOT)/uvm/sw/test/$(SW)
	endif
else
	MODULE = $(TB)

	ifeq ($(SW),)
		SW_DIR = $(PROJECT_ROOT)/uvm/sw/tb/$(TB)
	else
		SW_DIR = $(PROJECT_ROOT)/uvm/sw/tb/$(SW)
	endif
endif

# verify that the test or tb are provided
.PHONY: check_test_defined
check_test_defined:
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	if [ -z "$(TEST)" ] && [ -z "$(TB)" ]; then \
		logger ERROR "no simulation target specified: TEST=... (for pyuvm) or TB=... (for cocotb)."; \
		exit 1; \
	fi

CUSTOM_COMPILE_DEPS += check_test_defined

# ----------------------------------------------------------------------------------------------------------------------
# Test Software
# ----------------------------------------------------------------------------------------------------------------------

.PHONY: check_sw_dir_exists
check_sw_dir_exists:
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	if [ ! -d "$(SW_DIR)" ]; then \
		logger ERROR "test software directory not found in '$(SW_DIR)'"; \
		exit 1; \
	fi

CUSTOM_COMPILE_DEPS += check_sw_dir_exists

.PHONY: check_sw_dir_contains_main
check_sw_dir_contains_main:
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	if [ -z "$$(find $(SW_DIR) -name "main.c")" ]; then \
		logger ERROR "'main.c' not found in '$(SW_DIR)', software can not be compiled"; \
		exit 1; \
	fi

CUSTOM_COMPILE_DEPS += check_sw_dir_contains_main

# software
SW_MEM_HEX_FILE_PATH   	= $(SW_DIR)/build/verilog_hex.v
SW_IMEM1_HEX_FILE_PATH 	= $(SW_DIR)/build/instr_hex_1.mem
SW_IMEM2_HEX_FILE_PATH 	= $(SW_DIR)/build/instr_hex_2.mem
SW_DMEM_HEX_FILE_PATH  	= $(SW_DIR)/build/data_hex.mem

# pass the static paths to simulator to avoid recompilation
SW_PAYLOAD_DIR         = $(PROJECT_ROOT)/uvm/sim/sim_build/payload
SW_PAYLOAD_MEM_HEX     = $(SW_PAYLOAD_DIR)/verilog_hex.v
SW_PAYLOAD_IMEM1_HEX   = $(SW_PAYLOAD_DIR)/instr_hex_1.mem
SW_PAYLOAD_IMEM2_HEX   = $(SW_PAYLOAD_DIR)/instr_hex_2.mem
SW_PAYLOAD_DMEM_HEX    = $(SW_PAYLOAD_DIR)/data_hex.mem

.PHONY: build_sw
build_sw:
		@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
		$(MAKE) -C $(PROJECT_ROOT)/uvm/sw build SW_SOURCE_FULL_PATH=$(SW_DIR); \
		mkdir -p $(SW_PAYLOAD_DIR); \
		cp $(SW_MEM_HEX_FILE_PATH) $(SW_PAYLOAD_MEM_HEX); \
		cp $(SW_IMEM1_HEX_FILE_PATH) $(SW_PAYLOAD_IMEM1_HEX); \
		cp $(SW_IMEM2_HEX_FILE_PATH) $(SW_PAYLOAD_IMEM2_HEX); \
		cp $(SW_DMEM_HEX_FILE_PATH) $(SW_PAYLOAD_DMEM_HEX); \
		logger SUCCESS "binaries moved to payload directory '$(SW_PAYLOAD_DIR)'"

# load software before the simulation to prevent old software running on mcu with a different test
CUSTOM_COMPILE_DEPS += build_sw

.PHONY: set_sw_env
set_sw_env:
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	mkdir -p $(PROJECT_ROOT)/uvm/env; \
	. $(PROJECT_ROOT)/uvm/script/sw_mem_size.sh; \
	logger SUCCESS "software memory sizes extracted to '$(MCU_TEST_ENV_SW_MEM_SIZE_FILEPATH)'"

# used in mcu_test.py to configure memory mirror depending of the built test software in build_sw recipie
CUSTOM_COMPILE_DEPS += set_sw_env

# ----------------------------------------------------------------------------------------------------------------------
# Compilation Arguments
# ----------------------------------------------------------------------------------------------------------------------
ifeq ($(SIM), verilator)
	COMPILE_ARGS += -I$(PROJECT_ROOT)/rtl/include \
                -I$(PROJECT_ROOT)/rtl/peripherals \
                -I$(PROJECT_ROOT)/rtl/core \
                -I$(PROJECT_ROOT)/tb/misc

	COMPILE_ARGS += -f $(PROJECT_ROOT)/sim/rtl/files.f

	COMPILE_ARGS += -DNO_MODPORT_EXPRESSIONS -DFUNCTIONAL
	COMPILE_ARGS += --timescale-override 1ns/10ps

	COMPILE_ARGS += -Wno-MULTIDRIVEN -Wno-CASEINCOMPLETE -Wno-INITIALDLY \
				-Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-MULTITOP \
				-Wno-PINMISSING -Wno-MODDUP -Wno-IMPLICIT \
				-Wno-WIDTHCONCAT -Wno-UNOPTFLAT -Wno-SPECIFYIGN

	# aggresive optimization for speed
	COMPILE_ARGS += -O3

	# enable eeprom patch in tb/misc/24CS512.sv pathced file
	COMPILE_ARGS += -DVERILATOR_SIM_EEPROM_TIMING_PATCH

	# load compiled software program statically to dut
	COMPILE_ARGS += -DMEM_HEX_FILE=\"$(SW_PAYLOAD_MEM_HEX)\"
	COMPILE_ARGS += -DIMEM1_HEX_FILE=\"$(SW_PAYLOAD_IMEM1_HEX)\"
	COMPILE_ARGS += -DIMEM2_HEX_FILE=\"$(SW_PAYLOAD_IMEM2_HEX)\"
	COMPILE_ARGS += -DDMEM_HEX_FILE=\"$(SW_PAYLOAD_DMEM_HEX)\"
endif

ifeq ($(SIM), xcelium)
	# rtl file list
	COMPILE_ARGS += -f $(PROJECT_ROOT)/sim/rtl/files.f

	# preprocessor defines
	COMPILE_ARGS += -define FUNCTIONAL
	COMPILE_ARGS += -define MEM_HEX_FILE=\"$(SW_PAYLOAD_MEM_HEX)\"
	COMPILE_ARGS += -define IMEM1_HEX_FILE=\"$(SW_PAYLOAD_IMEM1_HEX)\"
	COMPILE_ARGS += -define IMEM2_HEX_FILE=\"$(SW_PAYLOAD_IMEM2_HEX)\"
	COMPILE_ARGS += -define DMEM_HEX_FILE=\"$(SW_PAYLOAD_DMEM_HEX)\"

	# suppress timing violations from pdk memory models because of the bootloader (not a design issue)
	COMPILE_ARGS += -notimingchecks
endif

# ----------------------------------------------------------------------------------------------------------------------
# Options
# ----------------------------------------------------------------------------------------------------------------------

ifeq ($(SIM), verilator)
	EXTRA_ARGS += --timing

	ifeq ($(WAVES),1)
		# Generate 'dump.vcd' waveform file
		EXTRA_ARGS += --trace --trace-structs
	endif

	ifeq ($(COV),1)
		EXTRA_ARGS += --coverage
	endif
endif

.PHONY: clean_xcelium_sim_files
clean_xcelium_sim_files:
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	rm -rf $(PROJECT_ROOT)/uvm/sim/sim_build; \
	rm -rf $(PROJECT_ROOT)/uvm/sim/cov_work; \
	logger SUCCESS "removed 'sim_build' and 'cov_work' directories"

ifeq ($(SIM), xcelium)
	EXTRA_ARGS += -access +rwc

	ifeq ($(GUI),1)
		# simvision reads wavefiles to show on gui
		WAVES := 1
		EXTRA_ARGS += +gui
	endif

	ifeq ($(WAVES),1)
		# dump waves in xcelium's native shm format and run
		EXTRA_ARGS += -input $(PROJECT_ROOT)/uvm/sim/xcelium/waves.tcl
	endif

	ifeq ($(COV),1)
		EXTRA_ARGS += -coverage all
	endif

	ifeq ($(CLEAN_RUN),1)
		run: clean_xcelium_sim_files
	endif
endif

.PHONY: tracer
tracer:
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	TRACER_LOG_FILE="$(PROJECT_ROOT)/uvm/sim/sim_build/tracer.log"; \
	if [ ! -f "$$TRACER_LOG_FILE" ]; then \
		logger ERROR "tracer log file '$$TRACER_LOG_FILE' not found, make sure the tracer is enabled in the test"; \
		exit 1; \
	fi; \
	watch -n 0.1 "tail -n $(TRACER_LINE_COUNT) $$TRACER_LOG_FILE"

# ----------------------------------------------------------------------------------------------------------------------
# Top
# ----------------------------------------------------------------------------------------------------------------------
VERILOG_SOURCES += $(PROJECT_ROOT)/uvm/rtl/mcu.sv

# ----------------------------------------------------------------------------------------------------------------------
# Cocotb / PyUVM
# ----------------------------------------------------------------------------------------------------------------------
export COCOTB_LOG_LEVEL ?= INFO

export PYUVM_LOG_LEVEL = $(LOG)

.PHONY: check_venv
check_venv:
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	if [ -z "$(VIRTUAL_ENV)" ]; then \
		logger ERROR "python's virtual environment not activated"; \
		logger INFO "run: 'source $(PROJECT_ROOT)/uvm/.venv/bin/activate'"; \
		exit 1; \
	fi

CUSTOM_COMPILE_DEPS += check_venv

ifeq ($(VIRTUAL_ENV),)
all: check_venv
else ifeq ($(MAKECMDGOALS),help)
# skip cocotb include when just printing help
else
include $(shell cocotb-config --makefiles)/Makefile.sim
endif

# ----------------------------------------------------------------------------------------------------------------------
# Custom
# ----------------------------------------------------------------------------------------------------------------------
# used by the McuTest in mcu_test.py and script/size.sh
export MCU_TEST_SW_DIR = $(SW_DIR)/build
export MCU_TEST_NAME = $(TEST)
export MCU_TEST_ENV_SW_MEM_SIZE_FILEPATH = $(PROJECT_ROOT)/uvm/env/sw_mem_size.env

# used in pyuvm tests for simulator-specific behavior handlin
export MCU_TEST_ENV_SIM = $(SIM)
