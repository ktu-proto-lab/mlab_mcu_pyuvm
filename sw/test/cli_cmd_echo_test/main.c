#include <stdint.h>
#include <stdbool.h>

#include "hal/gpio.c"
#include "hal/uart.c"
#include "sys/int.c"
#include "sys/time.c"
#include "io/printf.c"

// echo "mlab mcu"
#define CLI_MAX_ARGS 2

typedef void (*cli_command_handler_t)(int argc, char **argv);

typedef struct {
    const char *name;
    cli_command_handler_t handler;
} cli_command_t;

void cli_command_echo_handler(int argc, char **argv) {
    for (int i = 1; i < argc; ++i) {
        printf("%s", argv[i]);
    }
}

static const cli_command_t cli_command_table[] = {
    {"echo", cli_command_echo_handler}
};

static const uint32_t cli_command_count = sizeof(cli_command_table) / sizeof(cli_command_table[0]);

int string_compare(const char *lstring, const char *rstring) {
    while(*lstring && (*lstring == *rstring)) {
        lstring++;
        rstring++;
    }

    return *(uint8_t *)lstring - *(uint8_t *)rstring;
}

static bool receive_string(char *buffer, uint32_t lenght) {
    bool string_terminated = false;
    uint32_t count = 0;
    
    uart_rx_enable(&uart);
    while(count < lenght - 1) {
        uart_receive(&uart, (uint8_t *)&buffer[count], sizeof(uint8_t));
        if (buffer[count] == '\0') {
            string_terminated = true;
            break;
        }
        count++;
    }
    uart_rx_disable(&uart);
    
    return string_terminated;
}

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

uart_handle_t uart;
gpio_handle_t gpio;

int main() {
    gpio_init(&gpio);

    const uint32_t cpu_freq_mhz = 80;
    const uint32_t uart_baud_rate = 115200;
    uart.config.baud_rate = UART_BAUD_INTERVAL(cpu_freq_mhz, uart_baud_rate);
    uart.config.word_length = 0;
    uart.config.stop_bits = 0;
    uart.config.parity = 0;
    uart.config.parity_mode = 0;
    uart.config.parity_lock = 0;
    uart_init(&uart);
    gpio.regs->aux |= UART_GPIO_TX_PIN;
    gpio.regs->oe  |= UART_GPIO_TX_PIN;
    
    uart_tx_enable(&uart);
    uart_transmit(&uart, (uint8_t *)"ack", sizeof("ack"));
    uart_tx_disable(&uart);

    char buffer[256];
    receive_string(buffer, sizeof(buffer));

    time_delay_microseconds(5, cpu_freq_mhz);
    uart_tx_enable(&uart);
    cli_execute_command((char *)buffer);
    uart_tx_disable(&uart);
    while(1);
}
