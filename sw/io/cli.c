#include "io/cli.h"

#include <stdint.h>
#include "io/printf.h"
#include "lib/string.h"

typedef void (*cli_command_handler_t)(int argc, char **argv);

typedef struct {
    const char *name;
    cli_command_handler_t handler;
} cli_command_t;

static void cli_command_echo_handler(int argc, char **argv) {
    for (int i = 1; i < argc; ++i) {
        printf("%s", argv[i]);
    }
}

static const cli_command_t cli_command_table[] = {
    {"echo", cli_command_echo_handler}
};

static const uint32_t cli_command_count = sizeof(cli_command_table) / sizeof(cli_command_table[0]);

void cli_execute_command(char *input_buffer) {
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

    for (uint32_t i = 0; i < cli_command_count; ++i) {
        if (string_compare(argv[0], cli_command_table[i].name) == 0) {
            cli_command_table[i].handler(argc, argv);
            return;
        }
    }

    printf("Command not found: %s\n", argv[0]);
}
