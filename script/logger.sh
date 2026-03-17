#!/bin/bash
set -euo pipefail

if [[ -z "${_PROJECT_SCRIPT_LOGGER_SH_INCLUDED:-}" ]]; then
  _PROJECT_SCRIPT_LOGGER_SH_INCLUDED=1

readonly _PROJECT_SCRIPT_LOGGER_SH_SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

function logger {

  if [[ $# -eq 0 || $1 == "--help" ]]; then
      cat <<EOF
###########################################################

Function name: logger
Source file: $_PROJECT_SCRIPT_LOGGER_SH_SCRIPT_DIR/$(basename "$0")

Prints colored log messages with formatted flags

Usage:
  logger FLAG "message"
  logger --help

Example:
  logger INFO "system initialized"
  logger ERROR "failed to load config"

Supported FLAG values:
  $(logger FLAG "no background")
  $(logger INFO "white background (dark on light theme)")
  $(logger SUCCESS "green background")
  $(logger ERROR "red background")
  $(logger WARNING "yellow background")
  $(logger DEBUG "blue background")

###########################################################
EOF
    return 0
  fi

  # See: https://medium.com/@vitorcosta.matias/print-coloured-texts-in-console-a0db6f589138 (last checked on: 07.03.26)
  local -r NO_BACKGROUND=0
  local -r WHITE_BACKGROUND=7
  local -r RED_BACKGROUND=41
  local -r GREEN_BACKGROUND=42
  local -r YELLOW_BACKGROUND=43
  local -r BLUE_BACKGROUND=44

  local -r FLAG=$1

  LOG_FLAG_COLOR=$NO_BACKGROUND
  case $FLAG in
  INFO)
    LOG_FLAG_COLOR=$WHITE_BACKGROUND
    ;;
  SUCCESS)
    LOG_FLAG_COLOR=$GREEN_BACKGROUND
    ;;
  ERROR)
    LOG_FLAG_COLOR=$RED_BACKGROUND
    ;;
  DEBUG)
    LOG_FLAG_COLOR=$BLUE_BACKGROUND
    ;;
  WARNING)
    LOG_FLAG_COLOR=$YELLOW_BACKGROUND
    ;;
  esac

  local -r BEGIN_COLOR="\033[1;${LOG_FLAG_COLOR}m"
  local -r END_COLOR="\033[0m"
  local -r ALIGN_SIZE=7
  local -r RIGHT_ALIGN="+"
  local -r FLAG_FORMAT="%${RIGHT_ALIGN}${ALIGN_SIZE}s"
  local -r FLAG_PREFIX="${BEGIN_COLOR}[${FLAG_FORMAT}]${END_COLOR}"
  local -r TEXT=$2

  printf "${FLAG_PREFIX}: %s\\n" "$FLAG" "$TEXT"
}

fi
