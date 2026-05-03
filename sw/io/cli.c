#include "io/cli.h"

#include <stdint.h>
#include "io/printf.h"
#include "lib/string.h"
#include "sys/mem.h"
#include "sys/err.h"
#include "hal/gpio.h"

static system_error_t cli_echo_handler(int argc, char **argv) {
    if (argc != CLI_CMD_ECHO_ARG_COUNT) {
        return SYSTEM_ERROR_CLI_CMD_ECHO_INVALID_ARG_COUNT;
    }
    for (int i = 1; i < argc; ++i) {
        printf("%s", argv[i]);
    }
    return SYSTEM_ERROR_NONE;
}

static system_error_t cli_mem_read_handler(int argc, char **argv) {
    if (argc != CLI_CMD_MEM_READ_ARG_COUNT) {
        return SYSTEM_ERROR_CLI_CMD_MEM_READ_INVALID_ARG_COUNT;
    }
    uint32_t addr;
    if (!string_hex_to_uint(argv[2], &addr)) {
       return SYSTEM_ERROR_CLI_CMD_MEM_READ_INVALID_ADDR_HEX_FORMAT;
    }
    if (!SYSTEM_MEMORY_ADDR_VALID(addr)) {
        return SYSTEM_ERROR_CLI_CMD_MEM_READ_INVALID_ADDR;
    }
    uint32_t value = *((volatile uint32_t *)addr);
    printf("%x\n", value);
    return SYSTEM_ERROR_NONE;
}

static system_error_t cli_mem_write_handler(int argc, char **argv) {
    if (argc != CLI_CMD_MEM_WRITE_ARG_COUNT) {
        return SYSTEM_ERROR_CLI_CMD_MEM_WRITE_INVALID_ARG_COUNT;
    }
    uint32_t addr;
    if (!string_hex_to_uint(argv[2], &addr)) {
        return SYSTEM_ERROR_CLI_CMD_MEM_WRITE_INVALID_ADDR_HEX_COUNT;
    }
    if (!SYSTEM_MEMORY_ADDR_VALID(addr)) {
        return SYSTEM_ERROR_CLI_CMD_MEM_WRITE_INVALID_ADDR;
    }
    uint32_t new_value;
    if (!string_hex_to_uint(argv[3], &new_value)) {
        return SYSTEM_ERROR_CLI_CMD_MEM_WRITE_INVALID_VALUE_HEX_FORMAT;
    }
    uint32_t prev_value = *((volatile uint32_t *)addr);
    *((volatile uint32_t *)addr) = new_value;
    printf("%x\n", prev_value);
    return SYSTEM_ERROR_NONE;
}

static system_error_t cli_mem_dump_handler(int argc, char **argv) {
    if (argc != CLI_CMD_MEM_DUMP_ARG_COUNT) {
        return SYSTEM_ERROR_CLI_CMD_MEM_DUMP_INVALID_ARG_COUNT;
    }
    uint32_t addr;
    if (!string_hex_to_uint(argv[2], &addr)) {
        return SYSTEM_ERROR_CLI_CMD_MEM_DUMP_INVALID_ADDR_HEX_FORMAT;
    }
    if (!SYSTEM_MEMORY_ADDR_VALID(addr)) {
        return SYSTEM_ERROR_CLI_CMD_MEM_DUMP_INVALID_ADDR;
    }
    uint32_t word_count;
    if (!string_hex_to_uint(argv[3], &word_count)) {
        return SYSTEM_ERROR_CLI_CMD_MEM_DUMP_INVALID_WORD_COUNT_HEX_FORMAT;
    }
    if (!SYSTEM_MEMORY_ADDR_VALID(addr + (word_count * SYSTEM_MEMORY_WORD_SIZE_BYTES) - SYSTEM_MEMORY_WORD_SIZE_BYTES)) {
        return SYSTEM_ERROR_CLI_CMD_MEM_DUMP_WORD_COUNT_EXCEED_MEMORY;
    }
    volatile uint32_t *start = (uint32_t *)addr;
    const uint32_t *end = (uint32_t *)addr + word_count;
    if (start >= end) {
       return SYSTEM_ERROR_CLI_CMD_MEM_DUMP_START_ADDR_EXCEEDS_END_ADDR;
    }
    while(start < end) {
        uint32_t value = *start;
        // TODO (edit): end with a newline after test is updated
        printf("%x ", value);
        ++start;
    }
    printf("\n");
    return SYSTEM_ERROR_NONE;
}

static system_error_t cli_mem_cksum_handler(int argc, char **argv) {
    if (argc != CLI_CMD_MEM_CHECKSUM_ARG_COUNT) {
        return SYSTEM_ERROR_CLI_CMD_MEM_CHECKSUM_INVALID_ARG_COUNT;
    }
    uint32_t addr;
    if (!string_hex_to_uint(argv[2], &addr)) {
        return SYSTEM_ERROR_CLI_CMD_MEM_CHECKSUM_INVALID_ADDR_HEX_FORMAT;
    }
    if (!SYSTEM_MEMORY_ADDR_VALID(addr)) {
        return SYSTEM_ERROR_CLI_CMD_MEM_CHECKSUM_INVALID_ADDR;
    }
    uint32_t word_count;
    if (!string_hex_to_uint(argv[3], &word_count)) {
        return SYSTEM_ERROR_CLI_CMD_MEM_CHECKSUM_INVALID_WORD_COUNT_HEX_FORMAT;
    }
    if (!SYSTEM_MEMORY_ADDR_VALID(addr + (word_count * SYSTEM_MEMORY_WORD_SIZE_BYTES) - SYSTEM_MEMORY_WORD_SIZE_BYTES)) {
        return SYSTEM_ERROR_CLI_CMD_MEM_CHECKSUM_WORD_COUNT_EXCEED_MEMORY;
    }
    volatile uint32_t *start = (volatile uint32_t *)addr;
    uint32_t *end = (uint32_t *)addr + word_count;
    if (start >= end) {
        return SYSTEM_ERROR_CLI_CMD_MEM_CHECKSUM_START_ADDR_EXCEEDS_END_ADDR;
    }
    uint32_t checksum = *start;
    ++start;
    while (start < end) {
        checksum ^= (*start);
        ++start;
    }
    printf("%x\n", checksum);
    return SYSTEM_ERROR_NONE;
}

static system_error_t cli_mem_size_handler(int argc, char **argv) {
    if (argc != CLI_CMD_MEM_SIZE_ARG_COUNT) {
        return SYSTEM_ERROR_CLI_CMD_MEM_SIZE_INVALID_ARG_COUNT;
    }
    const char *type = argv[2];
    size_t size_bytes;
    if (string_compare(type, "imem") == 0) {
        size_bytes = SYSTEM_MEMORY_IMEM_SIZE;
    } else if (string_compare(type, "dmem") == 0) {
        size_bytes = SYSTEM_MEMORY_DMEM_SIZE;
    } else if (string_compare(type, "instr") == 0) {
        size_bytes = SYSTEM_MEMORY_PROGRAM_INSTR_SIZE_BYTES;
    } else if (string_compare(type, "ram") == 0) {
        size_bytes = SYSTEM_MEMORY_PROGRAM_RAM_SIZE_BYTES;
    } else if (string_compare(type, "bin") == 0) {
        size_bytes = SYSTEM_MEMORY_PROGRAM_BIN_SIZE_BYTES;
    } else if (string_compare(type, "text") == 0) {
        size_bytes = SYSTEM_MEMORY_PROGRAM_TEXT_SIZE_BYTES;
    } else if (string_compare(type, "data") == 0) {
        size_bytes = SYSTEM_MEMORY_PROGRAM_DATA_SIZE_BYTES;
    } else if (string_compare(type, "bss") == 0) {
        size_bytes = SYSTEM_MEMORY_PROGRAM_BSS_SIZE_BYTES;
    } else if (string_compare(type, "stack") == 0) {
        size_bytes = SYSTEM_MEMORY_PROGRAM_STACK_SIZE_BYTES;
    } else {
        return SYSTEM_ERROR_CLI_CMD_MEM_SIZE_UNKNOWN_ARG;
    }
    printf("%u\n", size_bytes);
    return SYSTEM_ERROR_NONE;
}

static system_error_t cli_mem_handler(int argc, char **argv) {
    if (argc < CLI_CMD_MEM_MIN_ARG_COUNT || argc > CLI_CMD_MEM_MAX_ARG_COUNT) {
        return SYSTEM_ERROR_CLI_CMD_MEM_INVALID_ARG_COUNT;
    }
    const char *subcmd = argv[1];
    if (string_compare(subcmd, "read") == 0) {
        return cli_mem_read_handler(argc, argv);
    } else if (string_compare(subcmd, "write") == 0) {
        return cli_mem_write_handler(argc, argv);
    } else if (string_compare(subcmd, "dump") == 0) {
        return cli_mem_dump_handler(argc, argv);
    } else if (string_compare(subcmd, "cksum") == 0) {
        return cli_mem_cksum_handler(argc, argv);
    } else if (string_compare(subcmd, "size") == 0) {
        return cli_mem_size_handler(argc, argv);
    } else {
        return SYSTEM_ERROR_CLI_CMD_MEM_SUBCMD_NOT_FOUND;
    }
}

static system_error_t cli_gpio_get_handler(int argc, char **argv) {
    if (argc != CLI_CMD_GPIO_GET_ARG_COUNT && argc != CLI_CMD_GPIO_GET_PIN_ARG_COUNT) {
        return SYSTEM_ERROR_CLI_CMD_GPIO_GET_INVALID_ARG_COUNT;
    }
    if (argc == CLI_CMD_GPIO_GET_ARG_COUNT) {
        // FIX: short fix for now, it should have a flag to indicate to apply uart mask or not
        uint32_t value = g_gpio.regs->in & ~(UART_GPIO_RX_PIN | UART_GPIO_TX_PIN);
        printf("%x\n", value);
        return SYSTEM_ERROR_NONE;
    }
    uint32_t pin;
    if (!string_hex_to_uint(argv[2], &pin)) {
        return SYSTEM_ERROR_CLI_CMD_GPIO_GET_INVALID_PIN_HEX_FORMAT;
    }
    uint32_t value = g_gpio.regs->in & (1 << pin) ? 1 : 0;
    printf("%u\n", value);
    return SYSTEM_ERROR_NONE;
}

static system_error_t cli_gpio_set_handler(int argc, char **argv) {
    if (argc != CLI_CMD_GPIO_SET_ARG_COUNT || argc != CLI_CMD_GPIO_SET_PIN_ARG_COUNT) {
        return SYSTEM_ERROR_CLI_CMD_GPIO_SET_INVALID_ARG_COUNT;
    }
    if (argc == CLI_CMD_GPIO_SET_ARG_COUNT) {
        uint32_t value;
        if (!string_hex_to_uint(argv[2], &value)) {
            return SYSTEM_ERROR_CLI_CMD_GPIO_SET_INVALID_VALUE_HEX_FORMAT;
        }
        uint32_t prev_value = g_gpio.regs->out;
        g_gpio.regs->out = value;
        printf("%x\n", prev_value);
        return SYSTEM_ERROR_NONE;
    }
    uint32_t pin;
    if (!string_hex_to_uint(argv[2], &pin)) {
        return SYSTEM_ERROR_CLI_CMD_GPIO_SET_INVALID_PIN_HEX_FORMAT;
    }
    uint32_t value;
    if (!string_hex_to_uint(argv[3], &value)) {
        return SYSTEM_ERROR_CLI_CMD_GPIO_SET_INVALID_VALUE_HEX_FORMAT;
    }
    uint32_t prev_value = g_gpio.regs->out & (1 << pin);
    if (value) {
        g_gpio.regs->out |= (1 << pin);
    } else {
        g_gpio.regs->out &= ~(1 << pin);
    }
    printf("%x\n", prev_value);
    return SYSTEM_ERROR_NONE;
}

static system_error_t cli_gpio_toggle_handler(int argc, char **argv) {
    if (argc != CLI_CMD_GPIO_TOGGLE_ARG_COUNT) {
        return SYSTEM_ERROR_CLI_CMD_GPIO_TOGGLE_INVALID_ARG_COUNT;
    }
    uint32_t pins;
    if (!string_hex_to_uint(argv[2], &pins)) {
        return SYSTEM_ERROR_CLI_CMD_GPIO_TOGGLE_INVALID_VALUE_HEX_FORMAT;
    }
    uint32_t prev_value = g_gpio.regs->out & pins;
    g_gpio.regs->out ^= pins;
    printf("%x\n", prev_value);
    return SYSTEM_ERROR_NONE;
}

static system_error_t cli_gpio_handler(int argc, char **argv) {
    const char *subcmd = argv[1];
    if (string_compare(subcmd, "get") == 0) {
        return cli_gpio_get_handler(argc, argv);
    } else if (string_compare(subcmd, "set") == 0) {
        return cli_gpio_set_handler(argc, argv);
    } else if (string_compare(subcmd, "toggle") == 0) {
        return cli_gpio_toggle_handler(argc, argv);
    } else {
        return SYSTEM_ERROR_CLI_CMD_MEM_SUBCMD_NOT_FOUND;
    }
}

typedef system_error_t (*cli_cmd_handler_t)(int argc, char **argv);

typedef struct {
    const char *name;
    cli_cmd_handler_t handler;
} cli_cmd_t;

static const cli_cmd_t cli_cmd_table[] = {
    {"echo", cli_echo_handler},
    {"mem", cli_mem_handler},
    {"gpio", cli_gpio_handler},
};

static const uint32_t cli_cmd_count = sizeof(cli_cmd_table) / sizeof(cli_cmd_table[0]);

system_error_t cli_exec(char *input_buffer) {
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

    if (argc <= 0 || argc > CLI_MAX_ARGS) {
        return SYSTEM_ERROR_CLI_INVALID_ARGUMENT_COUNT;
    }

    for (uint32_t i = 0; i < cli_cmd_count; ++i) {
        if (string_compare(argv[0], cli_cmd_table[i].name) == 0) {
            return cli_cmd_table[i].handler(argc, argv);
        }
    }

    return SYSTEM_ERROR_CLI_CMD_NOT_FOUND;
}
