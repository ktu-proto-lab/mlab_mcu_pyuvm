#include <stdint.h>

#include "hal/gpio.h"
#include "hal/uart.h"
#include "io/cli.h"
#include "io/printf.h"
#include "lib/string.h"
#include "sys/int.h"
#include "sys/time.h"
#include "sys/err.h"
#include "sys/state.h"

uart_handle_t uart;
gpio_handle_t gpio;

static void clear_buffer(char *buffer, uint32_t size) {
    for (uint32_t i = 0; i < size; ++i) {
        buffer[i] = 0;
    }
}

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
    gpio.regs->aux  |= UART_GPIO_TX_PIN;
    gpio.regs->oe   |= UART_GPIO_TX_PIN;
    gpio.regs->oe   |= SYSTEM_STATE_MASK;

    uart_tx_enable(&uart);
    // BUG: trying to enable rx like this stalls the test
    // uart_rx_enable(&uart);

    // BUG: smaller than 3 chars wide stalls the test, removing does too
    uart_transmit(&uart, "ack\n", 4);
    char buffer[256];
    while (1) {
        system_state_set(&gpio, SYSTEM_STATE_READY);
        // BUG: removing uart_rx/tx_enable stalls test
        uart_rx_enable(&uart);
        string_receive(buffer, sizeof(buffer));
        // BUG: removing with rx enable together
        uart_rx_disable(&uart);
        system_state_set(&gpio, SYSTEM_STATE_BUSY);
        system_error_t e = cli_exec(buffer);
        if (e != SYSTEM_ERROR_NONE) {
            system_error_print(e);
        }
        clear_buffer(buffer, sizeof(buffer));
    }
}

// heads up for mr. Zozin
#define SYS_INT_IMPL
#include "sys/int.h"
