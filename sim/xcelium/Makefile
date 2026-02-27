# ======================================================================================================================
# Xcelium Simulation Makefile
# ======================================================================================================================
# Usage:
#   make          - run simulation (no waveforms, terminal-only)
#   make WAVES=1  - capture waveforms
#   make GUI=1    - run in SimVision GUI
#   make clean    - remove simulation artifacts
# ======================================================================================================================

# ----------------------------------------------------------------------------------------------------------------------
# Simulator Configuration
# ----------------------------------------------------------------------------------------------------------------------
SIM = xcelium
TOPLEVEL_LANG = verilog

TOPLEVEL = mcu

TEST ?= gpio_4bit_mirror_test
MODULE = test.$(TEST)

# ----------------------------------------------------------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------------------------------------------------------
PROJECT_ROOT = $(shell pwd)/../../..

# Used by xrun to expand ${PROJECT_ROOT} inside files.f, solving the relative path mismatch between files.f and this 
# makefile location.
export PROJECT_ROOT

# Cocotb discovers Python testbench modules via PYTHONPATH, 'tb.py' lives in 'uvm/tb'.
export PYTHONPATH := $(PROJECT_ROOT)/uvm/tb:$(PYTHONPATH)

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

# ----------------------------------------------------------------------------------------------------------------------
# Options
# ----------------------------------------------------------------------------------------------------------------------

# SimVision GUI
GUI ?= 0

ifeq ($(GUI),1)
    # Requires wavefiles
    WAVES := 1
    EXTRA_ARGS += +gui
endif

# Do not generate waveform files by default for better performance
WAVES ?= 0

ifeq ($(WAVES),1)
		EXTRA_ARGS += -access +rw
endif

# ----------------------------------------------------------------------------------------------------------------------
# Top
# ----------------------------------------------------------------------------------------------------------------------
VERILOG_SOURCES += $(PROJECT_ROOT)/uvm/rtl/mcu.sv

# ----------------------------------------------------------------------------------------------------------------------
# Cocotb
# ----------------------------------------------------------------------------------------------------------------------
include $(shell cocotb-config --makefiles)/Makefile.sim
