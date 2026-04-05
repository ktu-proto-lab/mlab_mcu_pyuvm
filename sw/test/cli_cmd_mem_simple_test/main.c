#include <stdint.h>

#include "hal/gpio.h"
#include "hal/uart.h"
#include "io/cli.h"
#include "io/printf.h"
#include "lib/string.h"
#include "sys/int.h"
#include "sys/time.h"

uart_handle_t uart;
gpio_handle_t gpio;

#include "sys/int.c"

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
    gpio.regs->aux |= UART_GPIO_TX_PIN;
    gpio.regs->oe  |= UART_GPIO_TX_PIN;
    uart_tx_enable(&uart);
    uart_transmit(&uart, (uint8_t *)"ack", sizeof("ack"));
    // uart_tx_disable(&uart);
    char buffer[256];
    do {
        // uart_tx_enable(&uart);
        string_receive(buffer, sizeof(buffer));
        time_delay_microseconds(5, cpu_freq_mhz);
        cli_exec_cmd((char *)buffer);
        clear_buffer(buffer, sizeof(buffer));
        printf("[  DEBUG]: cleared buffer\n");
        // uart_tx_disable(&uart);
    } while(1);
}
