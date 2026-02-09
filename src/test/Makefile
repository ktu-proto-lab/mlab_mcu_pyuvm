SIM ?= verilator
TOPLEVEL_LANG ?= verilog

# TODO: maybe just run make from the script...
PROJECT_ROOT = $(shell pwd)/../../..

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

COMPILE_ARGS += -O0 -DVERILATOR_SIM_EEPROM_TIMING_PATCH

EXTRA_ARGS += --trace --trace-structs --no-trace-params --timing

VERILOG_SOURCES += $(PROJECT_ROOT)/uvm/src/rtl/mcu.sv

TOPLEVEL = mcu
MODULE = test

include $(shell cocotb-config --makefiles)/Makefile.sim