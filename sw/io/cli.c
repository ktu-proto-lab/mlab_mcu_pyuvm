#include "io/cli.h"

#include <stdint.h>
#include "io/printf.h"
#include "lib/string.h"

static void cli_cmd_echo_handler(int argc, char **argv) {
    for (int i = 1; i < argc; ++i) {
        printf("%s", argv[i]);
    }
}

static void cli_cmd_mem_handler(int argc, char **argv) {
    if (argc < 2) {
        return;
    }
    const char *subcmd = argv[1];
    // uint32_t addr = 0;
    // uint32_t value = 0;
    // // TODO: default is from the given address to the end
    // uint32_t word_cnt = 0;
    if (string_compare(subcmd, "read") == 0) {
        // mem read <addr>
        if (argc != 3) {
            return;
        }
        printf("[  DEBUG]: cmd mem read\n");
    } else if (string_compare(subcmd, "write") == 0) {
        // mem write <addr> <value>
        if (argc != 4) {
            return;
        }
        printf("[  DEBUG]: cmd mem write\n");
    } else if (string_compare(subcmd, "dump") == 0) {
        // mem dump <addr> [word_cnt]
        if (argc < 3) {
            return;
        }
        printf("[  DEBUG]: cmd mem dump\n");
    } else if (string_compare(subcmd, "checksum") == 0) {
        // mem checksum <addr> [word_cnt]
        if (argc < 3) {
            return;
        }
        printf("[  DEBUG]: cmd mem checksum\n");
    } else {
        printf("[  ERROR]: unknown mem sub-command '%s'\n", subcmd);
    }
}

typedef void (*cli_cmd_handler_t)(int argc, char **argv);

typedef struct {
    const char *name;
    cli_cmd_handler_t handler;
} cli_cmd_t;

static const cli_cmd_t cli_cmd_table[] = {
    {"echo", cli_cmd_echo_handler},
    {"mem", cli_cmd_mem_handler}
};

static const uint32_t cli_cmd_count = sizeof(cli_cmd_table) / sizeof(cli_cmd_table[0]);

void cli_exec_cmd(char *input_buffer) {
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
            cli_cmd_table[i].handler(argc, argv);
            return;
        }
    }

    printf("[  ERROR]: cmd not found: %s\n", argv[0]);
}
