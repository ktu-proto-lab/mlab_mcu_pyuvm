SHELL := /bin/bash
.SHELLFLAGS := -euo pipefail -c

export PROJECT_ROOT = $(abspath ../..)

define HELP_USAGE
-------------------------------------------------------------------------------
Builds C MCU firmware from a given source directory.

Usage:
	make [build] SW_SOURCE_DIR=<relative_path>
	make [build] SW_SOURCE_FULL_PATH=<absolute_path>

Targets:
    build   : cleans and compiles the firmware at the given source directory
    help    : show this message (default)

Options:
    SW_SOURCE_DIR           : path to the firmware source directory,
                              relative to 'project_root/uvm/sw/'.

    SW_SOURCE_FULL_PATH     : absolute path to the firmware source directory
                              passed in by the parent UVM sim makefile,
                              but can also be used directly.

Example:
	make SW_SOURCE_DIR=test/mcu_base_test
	make SW_SOURCE_FULL_PATH=/home/user/mlab_mcu/uvm/test/mcu_base_test
-------------------------------------------------------------------------------
endef
export HELP_USAGE

.PHONY: help
help:
	@echo "$$HELP_USAGE"

.DEFAULT_GOAL := help

.PHONY: build
build:
ifndef SW_SOURCE_FULL_PATH
ifndef SW_SOURCE_DIR
	$(error either SW_SOURCE_DIR or SW_SOURCE_FULL_PATH must be defined)
endif
	$(eval SW_SOURCE_FULL_PATH := $(PROJECT_ROOT)/uvm/sw/$(SW_SOURCE_DIR))
endif
	@set -e; \
	source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	if [ -d "$(SW_SOURCE_FULL_PATH)" ]; then \
		logger INFO "building software from $(SW_SOURCE_FULL_PATH)"; \
		$(MAKE) -C $(SW_SOURCE_FULL_PATH) clean; \
		$(MAKE) -C $(SW_SOURCE_FULL_PATH); \
		logger SUCCESS "$(SW_SOURCE_FULL_PATH) built"; \
	else \
		logger ERROR "software source directory '$(SW_SOURCE_FULL_PATH)' not found"; \
		exit 1; \
	fi
