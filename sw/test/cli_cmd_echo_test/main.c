#include <stdint.h>

#include "hal/gpio.c"
#include "hal/uart.c"
#include "sys/int.c"
#include "sys/time.c"

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
    const char *ack = "ack";
    uart_transmit(&uart, (uint8_t *)ack, sizeof(ack));
    uart_tx_disable(&uart);

    uint8_t buffer[12];
    uart_rx_enable(&uart);
    uart_receive(&uart, buffer, sizeof(buffer));

    time_delay_microseconds(5, cpu_freq_mhz);
    uart_tx_enable(&uart);
    uart_transmit(&uart, buffer, sizeof(buffer));
    uart_tx_disable(&uart);
    while(1);
}
