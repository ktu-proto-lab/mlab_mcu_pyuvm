PROGRAM = gpio_heartbeat

PROJECT_ROOT = $(shell pwd)/../../../../..

COMMON_DIR = $(PROJECT_ROOT)/sw/ibex/common

# All other source files are include in the main.c (single-source build approach)
C_SOURCES = \
	main.c 	

C_INCLUDES = \
	-Icore/inc \
	-I$(PROJECT_ROOT)/uvm/sw/hal \
	-I$(PROJECT_ROOT)/uvm/sw/soc
	
include $(COMMON_DIR)/common.mk
