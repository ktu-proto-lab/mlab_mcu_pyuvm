# ======================================================================================================================
# Simulation Makefile
# ======================================================================================================================
# Verilator
# ======================================================================================================================
# Usage:
#   make SIM=verilator 					- explicitly run on Verilator (no waveforms, terminal-only)
#   make SIM=verilator WAVES=1  		- capture waveforms (dump.vcd)
#   make SIM=verilator clean    		- remove simulation artifacts
# ======================================================================================================================
# Xcelium
# ======================================================================================================================
# Usage:
#   make SIM=xcelium				- run simulation on Xcelium (no waveforms, terminal-only)
#   make SIM=xcelium WAVES=1  		- capture waveforms
#   make SIM=xcelium GUI=1    		- run in SimVision GUI (waves are captured too)
#   make SIM=xcelium clean    		- remove simulation artifacts
# ======================================================================================================================
# Cocotb
# ======================================================================================================================
# 	make LOG=INFO		- print logs of the testbench (levels: TRACE, DEBUG, default: INFO, WARNING, ERROR, FATAL)
# ======================================================================================================================
# Examples
# ======================================================================================================================
# Run on Verilator, pyuvm test with log level as TRACE and dump waveforms to 'dump.vcd':
#
#	make SIM=verilator TEST=gpio.gpio_mirror_test LOG=TRACE WAVES=1
#
# Run on Cadence Xcelium, cocotb testbench via SimVisio GUI
#	make SIM=xcelium TB=simple_uart_tb.py GUI=1
# 
# Run on Verilator, cocotb testbench
# 	make TB=uart_simple
# ======================================================================================================================

# force to use bash
SHELL := /bin/bash

# prevent from building sw with custom makefile exiting early when sw compilation finishes 
.DEFAULT_GOAL := all

# ----------------------------------------------------------------------------------------------------------------------
# Options
# ----------------------------------------------------------------------------------------------------------------------
SIM ?= verilator

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

# ----------------------------------------------------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------------------------------------------------
TOPLEVEL_LANG = verilog

TOPLEVEL = mcu

# ----------------------------------------------------------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------------------------------------------------------
PROJECT_ROOT = $(abspath ../..)

# Used by: 
# the rtl's 'files.f' for Xcelium compatibility
# makefiles of the c code
export PROJECT_ROOT

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
		if [ -d "$(SW_DIR)" ]; then \
			logger INFO "building test software for $(TEST) in $(SW_DIR)"; \
			$(MAKE) -C $(SW_DIR) clean; \
			$(MAKE) -C $(SW_DIR); \
			logger INFO "copying software to static 'sim/sim_build/payload' directory"; \
			mkdir -p $(SW_PAYLOAD_DIR); \
			cp $(SW_MEM_HEX_FILE_PATH) $(SW_PAYLOAD_MEM_HEX); \
			cp $(SW_IMEM1_HEX_FILE_PATH) $(SW_PAYLOAD_IMEM1_HEX); \
			cp $(SW_IMEM2_HEX_FILE_PATH) $(SW_PAYLOAD_IMEM2_HEX); \
			cp $(SW_DMEM_HEX_FILE_PATH) $(SW_PAYLOAD_DMEM_HEX); \
		else \
			logger ERROR "test software directory '$(SW_DIR)' not found, could not compile, exiting"; \
			exit 1; \
		fi

# load software before the simulation to prevent old software running on mcu with a different test
CUSTOM_COMPILE_DEPS += build_sw

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
endif

ifeq ($(SIM), xcelium)
	ifeq ($(GUI),1)
		# SimVision reads wavefiles to show on GUI
		WAVES := 1
		EXTRA_ARGS += +gui
	endif

	ifeq ($(WAVES),1)
		EXTRA_ARGS += -access +rw
	endif
endif

# ----------------------------------------------------------------------------------------------------------------------
# Top
# ----------------------------------------------------------------------------------------------------------------------
VERILOG_SOURCES += $(PROJECT_ROOT)/uvm/rtl/mcu.sv

# ----------------------------------------------------------------------------------------------------------------------
# Cocotb
# ----------------------------------------------------------------------------------------------------------------------
export COCOTB_LOG_LEVEL ?= $(LOG)

include $(shell cocotb-config --makefiles)/Makefile.sim
