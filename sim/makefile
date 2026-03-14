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
# 	make LOG_LEVEL=INFO		- print logs of the testbench (levels: TRACE, DEBUG, default: INFO, WARNING, ERROR, FATAL)
# ======================================================================================================================
# Examples
# ======================================================================================================================
# Run on Verilator, pyuvm test with log level as TRACE and dump waveforms to 'dump.vcd':
#
#	make SIM=verilator TEST=gpio.gpio_mirror_test LOG_LEVEL=TRACE WAVES=1
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
LOG_LEVEL ?= INFO

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

ifeq ($(TB),)
	# gpio.mirror => TEST_GROUP=gpio, TEST_NAME=mirror
	TEST_GROUP := $(word 1, $(subst ., ,$(TEST)))
	TEST_NAME  := $(word 2, $(subst ., ,$(TEST)))
	MODULE = tb.test.$(TEST_GROUP).$(TEST_NAME)

	ifeq ($(SW),)
		# TEST=gpio.mirror => SW_TEST_PATH=uvm/sw/test/gpio/mirror
		SW_TEST_DIR_PATH = $(PROJECT_ROOT)/uvm/sw/test/$(TEST_GROUP)/$(TEST_NAME)
	else
		SW_TEST_DIR_PATH = $(PROJECT_ROOT)/uvm/sw/test/$(SW)
	endif
else
	MODULE = tb.$(TB)

	ifeq ($(SW),)
		SW_TEST_DIR_PATH = $(PROJECT_ROOT)/uvm/sw/tb/$(TB)
	else
		SW_TEST_DIR_PATH = $(PROJECT_ROOT)/uvm/sw/tb/$(SW)
	endif
endif

PROJECT_ROOT = $(shell pwd)/../..

# Used by the rtl's 'files.f' for Xcelium compatibility
export PROJECT_ROOT

# Cocotb discovers Python testbench modules via PYTHONPATH
export PYTHONPATH := $(PROJECT_ROOT)/uvm:$(PYTHONPATH)

# ----------------------------------------------------------------------------------------------------------------------
# Test
# ----------------------------------------------------------------------------------------------------------------------

# software
SW_MEM_HEX_FILE_PATH   	= $(SW_TEST_DIR_PATH)/build/verilog_hex.v
SW_IMEM1_HEX_FILE_PATH 	= $(SW_TEST_DIR_PATH)/build/instr_hex_1.mem
SW_IMEM2_HEX_FILE_PATH 	= $(SW_TEST_DIR_PATH)/build/instr_hex_2.mem
SW_DMEM_HEX_FILE_PATH  	= $(SW_TEST_DIR_PATH)/build/data_hex.mem

# pass the static paths to simulator to avoid recompilation
SW_PAYLOAD_DIR         = $(PROJECT_ROOT)/uvm/sim/payload
SW_PAYLOAD_MEM_HEX     = $(SW_PAYLOAD_DIR)/verilog_hex.v
SW_PAYLOAD_IMEM1_HEX   = $(SW_PAYLOAD_DIR)/instr_hex_1.mem
SW_PAYLOAD_IMEM2_HEX   = $(SW_PAYLOAD_DIR)/instr_hex_2.mem
SW_PAYLOAD_DMEM_HEX    = $(SW_PAYLOAD_DIR)/data_hex.mem

# compilation
.PHONY: build_test_sw
build_test_sw:
		@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
		if [ -d "$(SW_TEST_DIR_PATH)" ]; then \
			logger INFO "building test software for $(TEST_GROUP) -> $(TEST_NAME)"; \
			$(MAKE) -C $(SW_TEST_DIR_PATH) clean; \
			$(MAKE) -C $(SW_TEST_DIR_PATH); \
			logger INFO "copying software to static 'sim/payload' directory"; \
			mkdir -p $(SW_PAYLOAD_DIR); \
			cp $(SW_MEM_HEX_FILE_PATH) $(SW_PAYLOAD_MEM_HEX); \
			cp $(SW_IMEM1_HEX_FILE_PATH) $(SW_PAYLOAD_IMEM1_HEX); \
			cp $(SW_IMEM2_HEX_FILE_PATH) $(SW_PAYLOAD_IMEM2_HEX); \
			cp $(SW_DMEM_HEX_FILE_PATH) $(SW_PAYLOAD_DMEM_HEX); \
		else \
			logger ERROR "test software directory '$(SW_TEST_DIR_PATH)' not found, skipping compilation"; \
			exit 1; \
		fi

# load software before the simulation to prevent old software running on mcu with a different test
CUSTOM_COMPILE_DEPS += build_test_sw

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
export COCOTB_LOG_LEVEL ?= $(LOG_LEVEL)

include $(shell cocotb-config --makefiles)/Makefile.sim
