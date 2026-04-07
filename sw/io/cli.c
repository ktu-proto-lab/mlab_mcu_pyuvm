#include "io/cli.h"

#include <stdint.h>
#include "io/printf.h"
#include "lib/string.h"
#include "sys/mem.h"
#include "sys/err.h"

static system_error_t cli_cmd_echo_handler(int argc, char **argv) {
    if (argc < CLI_CMD_ECHO_ARG_COUNT) {
        return SYSTEM_ERROR_CLI_CMD_ECHO_INVALID_ARG_COUNT;
    }

    for (int i = 1; i < argc; ++i) {
        printf("%s", argv[i]);
    }

    return SYSTEM_ERROR_NONE;
}

static system_error_t cli_cmd_mem_handler(int argc, char **argv) {
    if (argc < CLI_CMD_MEM_MIN_ARG_COUNT) {
        return SYSTEM_ERROR_CLI_CMD_MEM_INVALID_ARG_COUNT;
    }

    const char *subcmd = argv[1];
    uint32_t addr;

    if (string_compare(subcmd, "read") == 0) {
        if (argc != CLI_CMD_MEM_READ_ARG_COUNT) {
            return SYSTEM_ERROR_CLI_CMD_MEM_READ_INVALID_ARG_COUNT;
        }

        if (!string_hex_to_uint(argv[2], &addr)) {
            return SYSTEM_ERROR_STRING_INVALID_HEX_FORMAT;
        }

        if (!SYS_MEM_ADDR_VALID(addr)) {
            return SYSTEM_ERROR_CLI_CMD_MEM_INVALID_ADDR;
        }

        uint32_t value = *((volatile uint32_t *)addr);

        printf("%x\n", value);

    } else if (string_compare(subcmd, "write") == 0) {
        // mem write <addr> <value>
        if (argc != 4) {
            return;
        }

        // TODO (refac): this should be nested with read sub-command to save some space
        if (!string_hex_to_uint(argv[2], &addr)) {
            return SYSTEM_ERROR_STRING_INVALID_HEX_FORMAT;
        }


        if (!SYS_MEM_ADDR_VALID(addr)) {
            return SYSTEM_ERROR_CLI_CMD_MEM_INVALID_ADDR;
        }

        uint32_t value;
        if (!string_hex_to_uint(argv[3], &value)) {
            return SYSTEM_ERROR_STRING_INVALID_HEX_FORMAT;
        }

        // TODO (refac): repeats identically like read sub-command
        uint32_t old_value = *((volatile uint32_t *)addr);

        // WARN: writing blindly, if it is writing on top of the actual program binaries - too bad
        *(volatile uint32_t *)addr = value;

        printf("%x\n", old_value);
    } else if (string_compare(subcmd, "dump") == 0) {
        // mem dump <addr> <word_count>
        if (argc < 4) {
            return;
        }

        if (!string_hex_to_uint(argv[2], &addr)) {
            return SYSTEM_ERROR_STRING_INVALID_HEX_FORMAT;
        }

        if (!SYS_MEM_ADDR_VALID(addr)) {
            return SYSTEM_ERROR_CLI_CMD_MEM_INVALID_ADDR;
        }

        uint32_t word_count;

        if (!string_hex_to_uint(argv[3], &word_count)) {
                return SYSTEM_ERROR_STRING_INVALID_HEX_FORMAT;
        }

        if (!SYS_MEM_ADDR_VALID(addr + (word_count * SYS_MEM_WORD_SIZE_BYTES) - SYS_MEM_WORD_SIZE_BYTES)) {
            return SYSTEM_ERROR_CLI_CMD_MEM_WORD_COUNT_EXCEED_MEMORY;
        }

        uint32_t *start = (uint32_t *)addr;
        const uint32_t *end = (uint32_t *)addr + word_count;
        
        while (start < end) {
            uint32_t value = *start;
            printf("%x ", value);
            start++;
        }
        printf("\n");

    } else if (string_compare(subcmd, "checksum") == 0) {
        // mem checksum <addr> [word_count]
        if (argc < 4) {
            return;
        }

        if (!string_hex_to_uint(argv[2], &addr)) {
            return SYSTEM_ERROR_STRING_INVALID_HEX_FORMAT;
        }

        if (!SYS_MEM_ADDR_VALID(addr)) {
            return SYSTEM_ERROR_CLI_CMD_MEM_INVALID_ADDR;
        }

        uint32_t word_count;

        if (!string_hex_to_uint(argv[3], &word_count)) {
                return SYSTEM_ERROR_STRING_INVALID_HEX_FORMAT;
        }

        if (!SYS_MEM_ADDR_VALID(addr + (word_count * SYS_MEM_WORD_SIZE_BYTES) - SYS_MEM_WORD_SIZE_BYTES)) {
            return SYSTEM_ERROR_CLI_CMD_MEM_WORD_COUNT_EXCEED_MEMORY;
        }

        uint32_t *start = (uint32_t *)addr;
        uint32_t *end = (uint32_t *)addr + word_count;
        uint32_t checksum = *start;
        ++start;

        while (start < end) {
            checksum ^= (*start);
            ++start;
        }
        
        printf("%x\n", checksum);
    } else {
        return SYSTEM_ERROR_CLI_CMD_MEM_SUBCMD_NOT_FOUND;
    }

    return SYSTEM_ERROR_NONE;
}

typedef system_error_t (*cli_cmd_handler_t)(int argc, char **argv);

typedef struct {
    const char *name;
    cli_cmd_handler_t handler;
} cli_cmd_t;

static const cli_cmd_t cli_cmd_table[] = {
    {"echo", cli_cmd_echo_handler},
    {"mem", cli_cmd_mem_handler}
};

static const uint32_t cli_cmd_count = sizeof(cli_cmd_table) / sizeof(cli_cmd_table[0]);

system_error_t cli_exec_cmd(char *input_buffer) {
    char *argv[CLI_MAX_ARGS];
    int argc = 0;
    bool in_word = false;
    bool in_quotes = false;
    uint32_t write_index = 0;

    for (uint32_t i = 0; input_buffer[i] != '\0'; ++i) {
        if (input_buffer[i] == '"') {
            in_quotes = !in_quotes;
            continue;
        }

        if (!in_quotes && input_buffer[i] == ' ') {
            input_buffer[write_index++] = '\0';
            in_word = false;
        } else {
            if (!in_word) {
                if (argc < CLI_MAX_ARGS) {
                    argv[argc++] = &input_buffer[write_index];
                }
                in_word = true;
            }
            input_buffer[write_index++] = input_buffer[i];
        }
    }

    input_buffer[write_index] = '\0';

    if (argc == 0) {
        return;
    }

    for (uint32_t i = 0; i < cli_cmd_count; ++i) {
        if (string_compare(argv[0], cli_cmd_table[i].name) == 0) {
            system_error_t e = cli_cmd_table[i].handler(argc, argv);
            if (e != SYSTEM_ERROR_NONE) {
                system_error_print(e);
            }
            // BUG
            return;
        }
    }

    return SYSTEM_ERROR_CLI_CMD_NOT_FOUND;
}
