# enforce single source define dependency
ifndef PROJECT_ROOT
    $(error PROJECT_ROOT is not defined)
endif

C_INCLUDES = -I$(PROJECT_ROOT)/uvm/sw
# append common sources to already listed ones
C_SOURCES += \
    $(PROJECT_ROOT)/uvm/sw/hal/gpio.c \
    $(PROJECT_ROOT)/uvm/sw/hal/uart.c \
    $(PROJECT_ROOT)/uvm/sw/io/cli.c \
    $(PROJECT_ROOT)/uvm/sw/io/printf.c \
    $(PROJECT_ROOT)/uvm/sw/lib/string.c \
    $(PROJECT_ROOT)/uvm/sw/sys/err.c \
    $(PROJECT_ROOT)/uvm/sw/sys/time.c

# used by the common.mk, do not touch, legacy compatibility
COMMON_DIR = $(PROJECT_ROOT)/sw/ibex/common
include $(COMMON_DIR)/common.mk
