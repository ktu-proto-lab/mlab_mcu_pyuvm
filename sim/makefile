# ======================================================================================================================
# Simulation Makefile
# ======================================================================================================================
# Verilator
# ======================================================================================================================
# Usage:
#   make SIM=verilator 	- explicitly run on Verilator (no waveforms, terminal-only)
#   make WAVES=1  		- capture waveforms (dump.vcd)
#   make clean    		- remove simulation artifacts
# ======================================================================================================================
# Xcelium
# ======================================================================================================================
# Usage:
#   make SIM=xcelium	- run simulation on Xcelium (no waveforms, terminal-only)
#   make WAVES=1  		- capture waveforms
#   make GUI=1    		- run in SimVision GUI (waves are captured too)
#   make clean    		- remove simulation artifacts
# ======================================================================================================================

# ----------------------------------------------------------------------------------------------------------------------
# Simulator Configuration
# ----------------------------------------------------------------------------------------------------------------------
SIM ?= verilator
TOPLEVEL_LANG = verilog

TOPLEVEL = mcu

TEST ?= gpio_mirror_test
MODULE = tb.test.gpio.$(TEST)

# ----------------------------------------------------------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------------------------------------------------------
PROJECT_ROOT = $(shell pwd)/../..

# Used by the rtl's 'files.f' for Xcelium compatibility
export PROJECT_ROOT

# Cocotb discovers Python testbench modules via PYTHONPATH
export PYTHONPATH := $(PROJECT_ROOT)/uvm:$(PYTHONPATH)

# ----------------------------------------------------------------------------------------------------------------------
# DUT's Test Program
# ----------------------------------------------------------------------------------------------------------------------

# WARNING: this points explicitly to the GPIO test program (24.02.26)
# TODO: proper test selection mechanism
MEM_HEX_FILE_PATH = $(PROJECT_ROOT)/uvm/sw/test/gpio/mirror/build/verilog_hex.v
IMEM1_HEX_FILE_PATH = $(PROJECT_ROOT)/uvm/sw/test/gpio/mirror/build/instr_hex_1.mem
IMEM2_HEX_FILE_PATH = $(PROJECT_ROOT)/uvm/sw/test/gpio/mirror/build/instr_hex_2.mem
DMEM_HEX_FILE_PATH = $(PROJECT_ROOT)/uvm/sw/test/gpio/mirror/build/data_hex.mem

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
	COMPILE_ARGS += -DRANDOM_NUMBER=$(shell echo $$((1 + RANDOM % 255)))
	COMPILE_ARGS += --timescale-override 1ns/10ps

	COMPILE_ARGS += -Wno-MULTIDRIVEN -Wno-CASEINCOMPLETE -Wno-INITIALDLY \
				-Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-MULTITOP \
				-Wno-PINMISSING -Wno-MODDUP -Wno-IMPLICIT \
				-Wno-WIDTHCONCAT -Wno-UNOPTFLAT -Wno-SPECIFYIGN

	# Aggresive optimization for speed
	COMPILE_ARGS += -O3

	# Enable EEPROM patch in tb/misc/24CS512.sv pathced file
	COMPILE_ARGS += -DVERILATOR_SIM_EEPROM_TIMING_PATCH

	# Load program to dut from provided path
	COMPILE_ARGS += -DMEM_HEX_FILE=\"$(MEM_HEX_FILE_PATH)\"
	COMPILE_ARGS += -DIMEM1_HEX_FILE=\"$(IMEM1_HEX_FILE_PATH)\"
	COMPILE_ARGS += -DIMEM2_HEX_FILE=\"$(IMEM2_HEX_FILE_PATH)\"
	COMPILE_ARGS += -DDMEM_HEX_FILE=\"$(DMEM_HEX_FILE_PATH)\"
endif

ifeq ($(SIM), xcelium)
	# RTL file list
	COMPILE_ARGS += -f $(PROJECT_ROOT)/sim/rtl/files.f

	# Preprocessor defines
	COMPILE_ARGS += -define FUNCTIONAL
	COMPILE_ARGS += -define RANDOM_NUMBER=$(shell echo $$((1 + RANDOM % 255)))
	COMPILE_ARGS += -define MEM_HEX_FILE=\"$(MEM_HEX_FILE_PATH)\"
	COMPILE_ARGS += -define IMEM1_HEX_FILE=\"$(IMEM1_HEX_FILE_PATH)\"
	COMPILE_ARGS += -define IMEM2_HEX_FILE=\"$(IMEM2_HEX_FILE_PATH)\"
	COMPILE_ARGS += -define DMEM_HEX_FILE=\"$(DMEM_HEX_FILE_PATH)\"

	# Suppress timing violations from PDK memory models because of the Bootloader (not a design issue)
	COMPILE_ARGS += -notimingchecks
endif

# ----------------------------------------------------------------------------------------------------------------------
# Options
# ----------------------------------------------------------------------------------------------------------------------
# Do not generate waveform files by default for better performance
WAVES ?= 0

ifeq ($(SIM), verilator)
	EXTRA_ARGS += --timing

	ifeq ($(WAVES),1)
		# Generate 'dump.vcd' waveform file
		EXTRA_ARGS += --trace --trace-structs
	endif
endif

ifeq ($(SIM), xcelium)
	# SimVision GUI
	GUI ?= 0

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
export COCOTB_LOG_LEVEL ?= INFO

include $(shell cocotb-config --makefiles)/Makefile.sim
