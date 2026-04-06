define HELP_USAGE
Build mlab mcu software from the 'uvm/sw' directory

Usage:
    make build <SW_SOURCE=<source_dir_path>|SW_SOURCE_FULL_PATH=<source_dir_full_path>>

Options:
    SW_SOURCE_FULL_PATH     : full path to the SW_SOURCE directory (used by the 'uvm/sim/makefile')
    SW_SOURCE               : SW_SW_SOURCE directory path in project's 'uvm/sw'

Example:
    make SW_SOURCE=test/mcu_base_test
    make SW_SOURCE_FULL_PATH=~/mlab_mcu/uvm/tb/gpio_simple_tb
endef
export HELP_USAGE

.PHONY: help
help:
	@echo "$$HELP_USAGE"

SHELL := /bin/bash

export PROJECT_ROOT = $(abspath ../..)

# TODO: rename SW_SOURCE full path
ifndef SW_SOURCE_FULL_PATH
    ifndef SW_SOURCE
        $(error either SW_SOURCE or SW_SOURCE_FULL_PATH must be defined)
    endif
    SW_SOURCE_FULL_PATH ?= $(PROJECT_ROOT)/uvm/sw/$(SW_SOURCE)
endif

.DEFAULT_GOAL := build

.PHONY: build
build:
	@set -e; \
	source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	if [ -d "$(SW_SOURCE_FULL_PATH)" ]; then \
		logger INFO "building software from $(SW_SOURCE_FULL_PATH)"; \
		$(MAKE) -C $(SW_SOURCE_FULL_PATH) clean; \
		$(MAKE) -C $(SW_SOURCE_FULL_PATH); \
		logger SUCCESS "$(SW_SOURCE_FULL_PATH) built"; \
	else \
		logger ERROR "SW_SOURCE directory $(SW_SOURCE_FULL_PATH) not found"; \
		exit 1; \
	fi
