#include "glob.h"

uart_handle_t uart;
gpio_handle_t gpio;

const uint32_t g_cpu_freq_mhz = 80;
const uint32_t g_uart_baud_rate = 115200;

void g_init(void) {
    gpio_init(&gpio);
    const uint32_t g_cpu_freq_mhz = 80;
    const uint32_t g_uart_baud_rate = 115200;
    uart.config.baud_rate = UART_BAUD_INTERVAL(g_cpu_freq_mhz, g_uart_baud_rate);
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
    uart_transmit(&uart, (uint8_t *)"ack\n", 4);
}
