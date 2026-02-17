SIM = xcelium
TOPLEVEL_LANG = verilog

TOPLEVEL = mcu
MODULE = tb


PROJECT_ROOT = $(shell pwd)/../..

# WARN: this points explicitly to the GPIO test program (17.02.26)
MEM_HEX_FILE_PATH = $(PROJECT_ROOT)/uvm/src/sw/gpio/build/verilog_hex.v

# Do not generate waveform files by default for better performance
WAVES ?= 0


COMPILE_ARGS += -I$(PROJECT_ROOT)/rtl/include 		\
                -I$(PROJECT_ROOT)/rtl/peripherals \
                -I$(PROJECT_ROOT)/rtl/core 				\
                -I$(PROJECT_ROOT)/tb/misc

COMPILE_ARGS += -f $(PROJECT_ROOT)/sim/rtl/files.f

COMPILE_ARGS += -DFUNCTIONAL 																					\
                -DRANDOM_NUMBER=$(shell echo $$((1 + RANDOM % 255))) 	\
                -define MEM_HEX_FILE=\"$(MEM_HEX_FILE_PATH)\"

# Ignore timing violations (from Bootloader)
COMPILE_ARGS += -notimingchecks

ifeq ($(WAVES),1)
		EXTRA_ARGS += -access +rw +gui
endif

VERILOG_SOURCES += $(PROJECT_ROOT)/uvm/src/rtl/mcu.sv

include $(shell cocotb-config --makefiles)/Makefile.sim