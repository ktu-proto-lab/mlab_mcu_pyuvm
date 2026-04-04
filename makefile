SHELL := /bin/bash

PROJECT_ROOT := $(abspath ..)
VERILATOR_NAME := Verilator v5.044
XCELIUM_NAME := Cadence Xcelium v24.03-s004

# match image tags in docker-compose.yml
USER_TAG := $(shell whoami)
IMAGE_VERILATOR := mlab-mcu-uvm-verilator-$(USER_TAG)
IMAGE_XCELIUM := mlab-mcu-uvm-cadence-$(USER_TAG)

export PROJECT_ROOT
export HOST_UID := $(shell id -u)
export HOST_GID := $(shell id -g)
export USER     := $(USER_TAG)

CADENCE_PATH := $(shell dirname $(shell dirname $(shell which xrun 2>/dev/null)) 2>/dev/null)

# ui helper
LOG := @source $(PROJECT_ROOT)/uvm/script/logger.sh; logger

define HELP_USAGE

Usage:
  make <tool>-<action>

Simulators:
  verilator  : $(VERILATOR_NAME), uses Docker engine
  xcelium    : $(XCELIUM_NAME), uses Podman engine

Actions:
  build      : build the container image
  setup      : initialize .venv and install pip requirements
  shell      : enter the container interactively
  stop       : stop and remove running containers
  purge      : remove the built image from the system

Examples:
  make verilator-build
  make xcelium-shell
  make xcelium-purge

endef
export HELP_USAGE


.PHONY: help clean guard-CADENCE_PATH
help:
	@echo "$$HELP_USAGE"

clean:
	$(LOG) INFO "cleaning local virtual environment"; \
	rm -rf .venv

guard-CADENCE_PATH:
	@if [ -z "$(CADENCE_PATH)" ]; then \
		$(LOG) ERROR "xrun not found in PATH, ensure Cadence tools are available on host."; \
		exit 1; \
	fi


# ----------------------------------------------------------------------------------------------------------------------
# Verilator (Docker Engine)
# ----------------------------------------------------------------------------------------------------------------------
.PHONY: verilator-build verilator-setup verilator-shell verilator-stop verilator-purge

verilator-build:
	$(LOG) INFO "building $(VERILATOR_NAME) image: $(IMAGE_VERILATOR)"; \
	docker compose build verilator

verilator-setup:
	$(LOG) INFO "installing dependencies inside $(VERILATOR_NAME) container"; \
	docker compose run --rm verilator /bin/bash -c \
		"python3 -m venv .venv && source .venv/bin/activate && pip install -r conf/requirements.txt"

verilator-shell:
	$(LOG) INFO "launching $(VERILATOR_NAME) shell (hostname: container-verilator)"; \
	docker compose run --rm verilator /bin/bash

verilator-stop:
	$(LOG) INFO "stopping Verilator containers..."; \
	docker compose down

verilator-purge: verilator-stop
	$(LOG) WARNING "removing image $(IMAGE_VERILATOR):latest"; \
	docker rmi $(IMAGE_VERILATOR):latest || true

# ----------------------------------------------------------------------------------------------------------------------
# Xcelium (Podman Engine)
# ----------------------------------------------------------------------------------------------------------------------
.PHONY: build-xcelium setup-xcelium shell-xcelium run-xcelium

xcelium-build: guard-CADENCE_PATH
	$(LOG) INFO "building $(XCELIUM_NAME) image: $(IMAGE_XCELIUM)"; \
	CADENCE_PATH=$(CADENCE_PATH) podman compose build xcelium

xcelium-setup: guard-CADENCE_PATH
	$(LOG) INFO "installing dependencies inside $(XCELIUM_NAME) container"; \
	CADENCE_PATH=$(CADENCE_PATH) podman compose run --rm xcelium /bin/bash -c \
		"python3 -m venv .venv && source .venv/bin/activate && pip install -r conf/requirements.txt"

xcelium-shell: guard-CADENCE_PATH
	$(LOG) INFO "launching $(XCELIUM_NAME) shell (hostname: container-xcelium)"; \
	CADENCE_PATH=$(CADENCE_PATH) podman compose run --rm xcelium /bin/bash

xcelium-stop: guard-CADENCE_PATH
	$(LOG) INFO "stopping Xcelium containers..."; \
	CADENCE_PATH=$(CADENCE_PATH) podman compose down

xcelium-purge: xcelium-stop
	$(LOG) WARNING "removing image $(IMAGE_XCELIUM):latest"; \
	podman rmi $(IMAGE_XCELIUM):latest || true

# TODO
# status:
# 	@echo "--- Docker (Verilator) Status ---"
# 	@docker ps -a --filter "name=mlab-mcu-uvm-verilator"
# 	@echo -e "\n--- Podman (Xcelium) Status ---"
# 	@podman ps -a --filter "name=mlab-mcu-uvm-xcelium"
