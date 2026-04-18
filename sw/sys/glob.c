#include "glob.h"

volatile uart_handle_t g_uart;
volatile gpio_handle_t g_gpio;

const uint32_t g_cpu_freq_mhz = 80;
const uint32_t g_uart_baud_rate = 115200;

void g_init(void) {
    gpio_init(&g_gpio);
    const uint32_t g_cpu_freq_mhz = 80;
    const uint32_t g_uart_baud_rate = 115200;
    g_uart.config.baud_rate = UART_BAUD_INTERVAL(g_cpu_freq_mhz, g_uart_baud_rate);
    g_uart.config.word_length = 0;
    g_uart.config.stop_bits = 0;
    g_uart.config.parity = 0;
    g_uart.config.parity_mode = 0;
    g_uart.config.parity_lock = 0;
    uart_init(&g_uart);
    g_gpio.regs->aux  |= UART_GPIO_TX_PIN;
    g_gpio.regs->oe   |= UART_GPIO_TX_PIN;
    g_gpio.regs->oe   |= SYSTEM_STATE_MASK;
    uart_tx_enable(&g_uart);
    // BUG: trying to enable rx like this stalls the test
    // uart_rx_enable(&uart);

    // BUG: smaller than 3 chars wide stalls the test, removing does too
    uart_transmit(&g_uart, (uint8_t *)"ack\n", 4);
}
