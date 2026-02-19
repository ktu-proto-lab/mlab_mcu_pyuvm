# ======================================================================================================================
# Verilator Simulation Makefile
# ======================================================================================================================
# Usage:
#   make          - run simulation (no waveforms, terminal-only)
#   make WAVES=1  - capture waveforms (dump.vcd)
#   make clean    - remove simulation artifacts
# ======================================================================================================================

# ----------------------------------------------------------------------------------------------------------------------
# Simulator Configuration
# ----------------------------------------------------------------------------------------------------------------------
SIM = verilator
TOPLEVEL_LANG = verilog

TOPLEVEL = mcu

TEST ?= gpio_basic_test
MODULE = test.$(TEST)

# ----------------------------------------------------------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------------------------------------------------------
PROJECT_ROOT = $(shell pwd)/../../..

# Used by the rtl's 'files.f' for Xcelium compatibility
export PROJECT_ROOT

# Cocotb discovers Python testbench modules via PYTHONPATH, 'tb.py' lives in 'uvm/tb'.
export PYTHONPATH := $(PROJECT_ROOT)/uvm/tb:$(PYTHONPATH)

# ----------------------------------------------------------------------------------------------------------------------
# DUT's Test Program
# ----------------------------------------------------------------------------------------------------------------------

# WARNING: this points explicitly to the GPIO test program (17.02.26)
# TODO: proper test selection mechanism
MEM_HEX_FILE_PATH = $(PROJECT_ROOT)/uvm/sw/gpio/build/verilog_hex.v

# ----------------------------------------------------------------------------------------------------------------------
# Compilation Arguments
# ----------------------------------------------------------------------------------------------------------------------
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
COMPILE_ARGS += --x-assign fast
COMPILE_ARGS += --x-initial fast
COMPILE_ARGS += --noassert
COMPILE_ARGS += --output-split 20000

# Enable EEPROM patch in tb/misc/24CS512.sv pathced file
COMPILE_ARGS += -DVERILATOR_SIM_EEPROM_TIMING_PATCH

# Load program to dut from provided path
COMPILE_ARGS += -DMEM_HEX_FILE=\"$(MEM_HEX_FILE_PATH)\"

# ----------------------------------------------------------------------------------------------------------------------
# Options
# ----------------------------------------------------------------------------------------------------------------------

# Do not generate 'dump.vcd' waveform file by default for better performance
WAVES ?= 0

EXTRA_ARGS += --timing

ifeq ($(WAVES),1)
    EXTRA_ARGS += --trace --trace-structs
endif

# ----------------------------------------------------------------------------------------------------------------------
# Top
# ----------------------------------------------------------------------------------------------------------------------
VERILOG_SOURCES += $(PROJECT_ROOT)/uvm/rtl/mcu.sv

# ----------------------------------------------------------------------------------------------------------------------
# Cocotb
# ----------------------------------------------------------------------------------------------------------------------
include $(shell cocotb-config --makefiles)/Makefile.sim