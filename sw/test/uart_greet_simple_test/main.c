#include <stdint.h>

#include "soc/gpio_regs.h"
#include "soc/uart_regs.h"

#include "hal/gpio.h"
#include "hal/uart.h"

#include "sys/time.h"

#include "hal/gpio.c"
#include "hal/uart.c"
#include "sys/int.c"
#include "sys/time.c"

int main() {
    gpio_handle_t gpio;
    gpio_init(&gpio);

    uart_handle_t uart;
    const uint32_t cpu_freq_mhz = 80;
    const uint32_t uart_baud_rate = 115200;
    uart.config.baud_rate = UART_BAUD_INTERVAL(cpu_freq_mhz, uart_baud_rate);
    uart.config.word_length = 0;
    uart.config.stop_bits = 0;
    uart.config.parity = 0;
    uart.config.parity_mode = 0;
    uart.config.parity_lock = 0;

    uart_init(&uart);

    gpio.regs->aux |= GPIO_PIN_1;
    gpio.regs->oe  |= GPIO_PIN_1;

    uint8_t buffer[] = "hello uart";
    uart_tx_enable(&uart);
    uart_transmit(&uart, buffer, 10);
    uart_tx_disable(&uart);

    uint8_t rx_buffer[10];
    uart_rx_enable(&uart);
    uart_receive(&uart, rx_buffer, 10);
    uart_rx_disable(&uart);

    uint8_t expected_rx_buffer[] = "hello back";
    for (uint8_t i = 0; i < 10; ++i) {
        if (rx_buffer[i] != expected_rx_buffer[i]) {
            time_delay_microseconds(5, cpu_freq_mhz);
            uint8_t tx_err[] = "error: bad msg";
            uart_tx_enable(&uart);
            uart_transmit(&uart, tx_err, 14);
            uart_tx_disable(&uart);
        }
    }

    time_delay_microseconds(5, cpu_freq_mhz);
    uint8_t tx_buffer[] = "roger that";
    uart_tx_enable(&uart);
    uart_transmit(&uart, tx_buffer, 11);
    uart_tx_disable(&uart);

    while(1);
}
