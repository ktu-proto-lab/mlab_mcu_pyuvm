#ifndef SW_IO_CLI_H
#define SW_IO_CLI_H

#include "sys/err.h"

#define CLI_MAX_ARGS 4

// TODO: actually 2, but mem test will be implemented in the future
#define CLI_CMD_MEM_MIN_ARG_COUNT 3UL

#define CLI_CMD_MEM_MAX_ARG_COUNT 4UL

// mem read <addr>
#define CLI_CMD_MEM_READ_ARG_COUNT 3UL
// mem write <addr> <val>
#define CLI_CMD_MEM_WRITE_ARG_COUNT 4UL
// mem dump <addr> <word_count>
#define CLI_CMD_MEM_DUMP_ARG_COUNT 4UL
// mem checksum <addr> <word_count>
#define CLI_CMD_MEM_CHECKSUM_ARG_COUNT 4UL

// echo "string"
#define CLI_CMD_ECHO_ARG_COUNT 2UL

system_error_t cli_exec_cmd(char *input_buffer);

#endif
