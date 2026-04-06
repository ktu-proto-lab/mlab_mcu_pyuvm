#ifndef SW_IO_CLI_H
#define SW_IO_CLI_H

#include "sys/err.h"

#define CLI_MAX_ARGS 4

// TODO: actually 2, but mem test will be implemented in the future
#define CLI_CMD_MEM_MIN_ARG_COUNT 3UL

// mem read <addr>
#define CLI_CMD_MEM_READ_ARG_COUNT 3UL

// echo "string"
#define CLI_CMD_ECHO_ARG_COUNT 2UL

system_error_t cli_exec_cmd(char *input_buffer);

#endif
