SHELL := /bin/bash
# exit immediatelly on errors, undefined variables, on pipeline fails
.SHELLFLAGS := -euo pipefail -c

PROJECT_ROOT = $(abspath ..)
VERILATOR_NAME = Verilator v5.044
XCELIUM_NAME = Cadence Xcelium v24.03-s004

VERILATOR_IMAGE   := mlab-mcu-uvm-verilator-$(shell whoami):latest
XCELIUM_IMAGE     := mlab-mcu-uvm-xcelium-$(shell whoami):latest

export CADENCE_ROOT := /eda/cadence/2024-25/RHELx86/XCELIUM_24.03.004
export PROJECT_ROOT
export HOST_UID := $(shell id -u)
export HOST_GID := $(shell id -g)
export USER     := $(shell whoami)

define HELP_USAGE
Usage:
  make <target>

Simulators:
  verilator  : $(VERILATOR_NAME)
  xcelium    : $(XCELIUM_NAME)

Verilator Actions:
  verilator-build-image         : build the Verilator Docker image
  verilator-setup-env         		: initialize venv and install requirements
  verilator-shell-container: enter the Verilator container

Xcelium Actions:
  xcelium-build-image     : build the Xcelium Podman image
  xcelium-setup-env       : initialize venv and install requirements
  xcelium-run-container   : enter the Xcelium container

Cleanup:
  verilator-purge         : remove local .venv and delete Verilator image
  xcelium-purge           : remove local .venv and delete Xcelium image

Patching:
  apply-patches           : apply uvm-specific patches to the RTL files
  reverse-patches         : reverse patches of the RTL files

Examples:
  make xcelium-build-image
  make xcelium-run-container
endef
export HELP_USAGE

.PHONY: help
help:
	@echo "$$HELP_USAGE"

# ----------------------------------------------------------------------------------------------------------------------
# Patching
# ----------------------------------------------------------------------------------------------------------------------
.PHONY: apply-patches reverse-patches

apply-patches:
	@. $(PROJECT_ROOT)/uvm/script/patcher.sh --apply

reverse-patches:
	@. $(PROJECT_ROOT)/uvm/script/patcher.sh --reverse

# ----------------------------------------------------------------------------------------------------------------------
# Verilator (Docker)
# ----------------------------------------------------------------------------------------------------------------------
.PHONY: verilator-build-image verilator-setup-env verilator-run-container verilator-purge

verilator-build-image:
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	logger INFO "building $(VERILATOR_NAME) image"; \
	docker compose build verilator; \
	logger SUCCESS "$(VERILATOR_NAME) image '$(VERILATOR_IMAGE)' built"

verilator-setup-env:
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	logger INFO "initializing the environment inside the $(VERILATOR_NAME) container"; \
	docker compose run --rm verilator /bin/bash -c \
		"python3 -m venv .venv && source .venv/bin/activate && pip install --upgrade pip && pip install -r conf/requirements.txt"; \
	logger SUCCESS "$(VERILATOR_NAME) environment setup done"

verilator-run-container:
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	logger INFO "entering $(VERILATOR_NAME) container shell"; \
	docker compose run --rm verilator \
		/bin/bash -c "source /home/mcu/uvm/script/logger.sh && logger SUCCESS 'you are inside $(VERILATOR_NAME) container'; exec bash"

verilator-purge:
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	logger INFO "deleting virtual environment '.venv'"; \
	rm -rf .venv; \
	logger INFO "removing $(VERILATOR_NAME) built image '$(VERILATOR_IMAGE)'"; \
	docker rmi $(VERILATOR_IMAGE); \
	logger SUCCESS "$(VERILATOR_NAME) purging successful"

# ----------------------------------------------------------------------------------------------------------------------
# Xcelium (Podman)
# ----------------------------------------------------------------------------------------------------------------------
.PHONY: xcelium-build-image xcelium-setup-env xcelium-run-container xcelium-purge

xcelium-build-image:
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	logger INFO "building $(XCELIUM_NAME) image"; \
	CADENCE_PATH=$(CADENCE_PATH) podman build -f ./sim/xcelium/dockerfile -t $(XCELIUM_IMAGE) .; \
	logger SUCCESS "$(XCELIUM_NAME) image '$(XCELIUM_IMAGE)' built"

xcelium-setup-env:
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	logger INFO "initializing $(XCELIUM_NAME) environment inside the container"; \
	CADENCE_PATH=$(CADENCE_PATH) podman compose run --rm xcelium /bin/bash -c \
		"python3 -m venv .venv && source .venv/bin/activate && pip install --upgrade pip && pip install -r conf/requirements.txt"; \
	logger SUCCESS "$(XCELIUM_NAME) environment setup done"

xcelium-run-container:
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	logger INFO "entering $(XCELIUM_NAME) container shell"; \
	export CADENCE_PATH=$(CADENCE_PATH); \
	export CDS_LIC_FILE=$(CDS_LIC_FILE); \
	podman compose run --rm xcelium \
		/bin/bash -c "source /home/mcu/uvm/script/logger.sh && logger SUCCESS 'you are inside $(XCELIUM_NAME) container'; exec bash"

xcelium-purge:
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	logger INFO "deleting virtual environment '.venv'"; \
	rm -rf .venv; \
	logger INFO "removing $(XCELIUM_NAME) built image '$(XCELIUM_IMAGE)'"; \
	podman rmi $(XCELIUM_IMAGE); \
	logger SUCCESS "$(XCELIUM_NAME) purging successful"
