PROGRAM = cli_cmd_echo_test

C_INCLUDES = -I$(PROJECT_ROOT)/uvm/sw

C_SOURCES = main.c \
			$(PROJECT_ROOT)/uvm/sw/hal/gpio.c \
			$(PROJECT_ROOT)/uvm/sw/hal/uart.c \
			$(PROJECT_ROOT)/uvm/sw/io/cli.c \
			$(PROJECT_ROOT)/uvm/sw/io/printf.c \
			$(PROJECT_ROOT)/uvm/sw/lib/string.c \
			$(PROJECT_ROOT)/uvm/sw/sys/time.c

COMMON_DIR = $(PROJECT_ROOT)/sw/ibex/common

include $(COMMON_DIR)/common.mk
