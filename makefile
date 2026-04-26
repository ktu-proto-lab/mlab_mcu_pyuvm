define HELP_USAGE
-------------------------------------------------------------------------------
Usage:
  make <action> <simulator> [options]

Simulators:
  verilator  : $(VERILATOR_NAME)
  xcelium    : $(XCELIUM_NAME)

Actions:
  image      : build the Docker/Podman image for the simulator
               options: [purge] to delete the image

  venv       : initialize venv and install requirements inside the container

  run        : enter the simulator container shell

  patch      : apply or referse compatibility patches of root project

Examples:
  make image xcelium
  make image verilator purge
  make venv verilator
  make run xcelium
  make patch apply
  make patch reverse
-------------------------------------------------------------------------------
endef
export HELP_USAGE
.DEFAULT_GOAL := help
.PHONY: help
help:
	@echo "$$HELP_USAGE"

SHELL := /bin/bash
.SHELLFLAGS := -euo pipefail -c

PROJECT_ROOT := $(abspath ..)
VERILATOR_NAME := Verilator v5.044
XCELIUM_NAME := Cadence Xcelium v24.03-s004

export PROJECT_ROOT
export HOST_UID := $(shell id -u)
export HOST_GID := $(shell id -g)
export USER := $(shell whoami)
# must match with names given in docker-compose.yml
VERILATOR_IMAGE := mlab-mcu-uvm-verilator-$(USER):latest
XCELIUM_IMAGE := mlab-mcu-uvm-xcelium-$(USER):latest
# used in docker-compose.yml
export CADENCE_ROOT := /eda/cadence/2024-25/RHELx86/XCELIUM_24.03.004

ACTIONS := image venv run purge patch
ACTION := $(firstword $(MAKECMDGOALS))
ifneq ($(filter $(ACTION),$(ACTIONS)),)
    ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
    $(eval $(ARGS):;@:)
endif

# make patch <apply|reverse>
PATCH_ACTION_OPTION := $(word 1, $(ARGS))
.PHONY: patch
patch:
ifeq ($(PATCH_ACTION_OPTION),apply)
	@. $(PROJECT_ROOT)/uvm/script/patcher.sh --apply
else ifeq ($(PATCH_ACTION_OPTION),reverse)
	@$(PROJECT_ROOT)/uvm/script/patcher.sh --reverse
else
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	logger ERROR "invalid patch option '$(PATCH_ACTION_OPTION)' provided, use 'make help'"; \
	exit 1
endif

# make image <verilator|xcelium> [purge]
# TODO: check if podman has rootless permissions before building or purging images, and provide instructions to the user if not
SIMULATOR := $(word 1, $(ARGS))
IMAGE_ACTION_OPTION := $(word 2, $(ARGS))
IMAGE_ACTION_OPTION_PURGE := purge
.PHONY: image
image:
ifeq ($(SIMULATOR),verilator)
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	if ! docker info >/dev/null 2>&1; then \
		logger WARNING "docker requires sudo, is not running, or user lacks permissions"; \
		if ! groups | grep -q docker; then \
			logger INFO "adding user '$(USER)' to docker group..."; \
			sudo usermod -aG docker "$(USER)"; \
			logger INFO "please log out and log back in, reboot, or run: 'newgrp docker'"; \
		fi; \
		exit 1; \
	fi; \
	if [ "$(IMAGE_ACTION_OPTION)" = "$(IMAGE_ACTION_OPTION_PURGE)" ]; then \
		logger INFO "purging $(VERILATOR_NAME) image"; \
		docker rmi $(VERILATOR_IMAGE); \
		logger SUCCESS "$(VERILATOR_NAME) image purged"; \
	elif [ -n "$(IMAGE_ACTION_OPTION)" ]; then \
		logger ERROR "invalid option '$(IMAGE_ACTION_OPTION)', use 'purge' or leave empty."; \
		exit 1; \
	else \
		logger INFO "building $(VERILATOR_NAME) image"; \
		docker compose build verilator; \
		logger SUCCESS "$(VERILATOR_NAME) image '$(VERILATOR_IMAGE)' built"; \
	fi
else ifeq ($(SIMULATOR),xcelium)
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	if ! command -v podman >/dev/null 2>&1; then \
		logger ERROR "podman is not installed or not in PATH"; \
		exit 1; \
	fi; \
	if [ "$(IMAGE_ACTION_OPTION)" = "$(IMAGE_ACTION_OPTION_PURGE)" ]; then \
		logger INFO "purging $(XCELIUM_NAME) image"; \
		podman rmi $(XCELIUM_IMAGE); \
		logger SUCCESS "$(XCELIUM_NAME) image purged"; \
	elif [ -n "$(IMAGE_ACTION_OPTION)" ]; then \
		logger ERROR "invalid option '$(IMAGE_ACTION_OPTION)', use 'purge' or leave empty"; \
		exit 1; \
	else \
		logger INFO "building $(XCELIUM_NAME) image"; \
		CADENCE_PATH=$(CADENCE_PATH) podman build -f ./sim/xcelium/dockerfile -t $(XCELIUM_IMAGE) .; \
		logger SUCCESS "$(XCELIUM_NAME) image '$(XCELIUM_IMAGE)' built"; \
	fi
else
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	logger ERROR "specify valid simulator: verilator or xcelium, use 'make help' to display usage"; \
	exit 1
endif

.PHONY: run
run:
ifeq ($(SIMULATOR),verilator)
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	XHOST_INFO="$$(xhost +local: 2>&1)"; \
	logger INFO "$$XHOST_INFO used for GTKWave"; \
	logger INFO "entering $(VERILATOR_NAME) container shell"; \
	docker compose run --rm verilator \
		/bin/bash -c "source /home/mcu/uvm/script/logger.sh && logger SUCCESS 'you are inside $(VERILATOR_NAME) container' && source /home/mcu/uvm/.venv/bin/activate && cd /home/mcu/uvm/sim && exec bash"
else ifeq ($(SIMULATOR),xcelium)
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	logger INFO "entering $(XCELIUM_NAME) container shell"; \
	export CADENCE_PATH=$(CADENCE_PATH); \
	export CDS_LIC_FILE=$(CDS_LIC_FILE); \
	podman compose run --rm xcelium \
		/bin/bash -c "source /home/mcu/uvm/script/logger.sh && logger SUCCESS 'you are inside $(XCELIUM_NAME) container'; exec bash"
else
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	logger ERROR "specify valid simulator to build image of: verilator or xcelium, use 'make help' to display usage"; \
	exit 1
endif

# make venv <verilator|xcelium|clean>
VENV_ACTION_OPTION := $(word 1, $(ARGS))
.PHONY: venv
venv:
ifeq ($(SIMULATOR),verilator)
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	logger INFO "initializing the environment inside the $(VERILATOR_NAME) container"; \
	docker compose run --rm verilator /bin/bash -c \
		"python3 -m venv .venv && source .venv/bin/activate && pip install --upgrade pip && pip install -r conf/requirements.txt"; \
	logger SUCCESS "$(VERILATOR_NAME) environment setup done"
else ifeq ($(SIMULATOR),xcelium)
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	logger INFO "initializing $(XCELIUM_NAME) environment inside the container"; \
	CADENCE_PATH=$(CADENCE_PATH) podman compose run --rm xcelium /bin/bash -c \
		"python3 -m venv .venv && source .venv/bin/activate && pip install --upgrade pip && pip install -r conf/requirements.txt"; \
	logger SUCCESS "$(XCELIUM_NAME) environment setup done"
else ifeq ($(VENV_ACTION_OPTION),clean)
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	rm -rf $(PROJECT_ROOT)/uvm/.venv; \
	logger SUCCESS "cleaned virtual environment (deleted '.venv' directory)"
else
	@source $(PROJECT_ROOT)/uvm/script/logger.sh; \
	logger ERROR "option '$(VENV_ACTION_OPTION)' not valid, use 'make help' to display usage"; \
	exit 1
endif
