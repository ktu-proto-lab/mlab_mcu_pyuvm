SHELL := /bin/bash

PROJECT_ROOT = $(abspath ..)
VERILATOR_NAME = Verilator v5.044
XCELIUM_NAME = Cadence Xcelium v24.03-s004

IMAGE_VERILATOR   := mlab-mcu-uvm-verilator-$(shell whoami):latest
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
  verilator-build         : build the Verilator Docker image
  verilator-setup         : initialize venv and install requirements
  verilator-shell         : enter the Verilator container

Xcelium Actions:
  xcelium-build-image     : build the Xcelium Podman image
  xcelium-setup-env       : initialize venv and install requirements
  xcelium-run-container   : enter the Xcelium container

Cleanup:
  clean                   : stop all containers and remove local .venv
  xcelium-purge           : remove local .venv and delete Xcelium image

Examples:
  make xcelium-build-image
  make xcelium-run-container
endef
export HELP_USAGE

.PHONY: help clean
help:
	@echo "$$HELP_USAGE"

clean:
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	docker compose down -v || true
	podman compose down -v || true
	rm -rf .venv


.PHONY: build-verilator setup-verilator shell-verilator run-verilator

verilator-build:
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	logger INFO "building $(VERILATOR_NAME) image"; \
	docker compose build verilator

verilator-setup:
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	logger INFO "initializing the environment inside the $(VERILATOR_NAME) container"; \
	docker compose run --rm verilator /bin/bash -c \
		"python3 -m venv .venv && source .venv/bin/activate && pip install --upgrade pip && pip install -r conf/requirements.txt"

verilator-shell:
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	logger INFO "entering $(VERILATOR_NAME) container shell"; \
	docker compose run --rm verilator /bin/bash

# ----------------------------------------------------------------------------------------------------------------------
# Xcelium (Podman Engine)
# ----------------------------------------------------------------------------------------------------------------------
.PHONY: build-xcelium setup-xcelium shell-xcelium run-xcelium

xcelium-build-image:
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	logger INFO "building $(XCELIUM_NAME) image"; \
	CADENCE_PATH=$(CADENCE_PATH) podman compose build xcelium; \
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
	logger SUCCESS "purging successful"
