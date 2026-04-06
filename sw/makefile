define HELP_USAGE
Build mlab mcu software from the 'uvm/sw' directory

Usage:
    make build SOURCE=<source_dir>

Options:
    SOURCE  : source directory path in 'uvm/sw'

Example:
    make SOURCE=test/mcu_base_test
    make SOURCE=tb/gpio_simple_tb
endef
export HELP_USAGE

.PHONY: help
help:
	@echo "$$HELP_USAGE"

SHELL := /bin/bash

export PROJECT_ROOT = $(abspath ../..)

ifndef SOURCE
    $(error SOURCE not defined)
endif

SOURCE_PATH ?= $(PROJECT_ROOT)/uvm/sw/$(SOURCE)

.PHONY: build
build:
	@set -e; \
	source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	if [ -d "$(SOURCE_PATH)" ]; then \
		logger INFO "building software from $(SOURCE_PATH)"; \
		$(MAKE) -C $(SOURCE_PATH) clean; \
		$(MAKE) -C $(SOURCE_PATH); \
		logger SUCCESS "$(SOURCE_PATH) built"; \
	else \
		logger ERROR "source directory $(SOURCE_PATH) not found"; \
		exit 1; \
	fi
