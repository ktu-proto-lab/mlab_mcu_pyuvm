#include <stdint.h>

#include "hal/gpio.h"
#include "hal/uart.h"
#include "io/printf.h"
#include "sys/int.h"

uart_handle_t uart;
gpio_handle_t gpio;

int main() {
    gpio_init(&gpio);
    gpio.regs->aux |= GPIO_PIN_1;
    gpio.regs->oe  |= GPIO_PIN_1;

    const uint32_t cpu_freq_mhz = 80;
    const uint32_t uart_baud_rate = 115200;
    uart.config.baud_rate = UART_BAUD_INTERVAL(cpu_freq_mhz, uart_baud_rate);
    uart.config.word_length = 0;
    uart.config.stop_bits = 0;
    uart.config.parity = 0;
    uart.config.parity_mode = 0;
    uart.config.parity_lock = 0;
    uart_init(&uart);
    uart_tx_enable(&uart);

    // printf: s: string, int: 189, int: -9021, uint: 1926478, int: 0, uint: 0, char: h, %r
    const char *string = "string";
    const int positive_integer = 189;
    const int negative_integer = -9021;
    const unsigned int unsigned_integer = 1926478;
    const int zero_integer = 0;
    const unsigned int unsigned_zero_integer = 0;
    const char character = 'h';
    const char *unknown_format = "fmt";
    printf("printf: s: %s, int: %i, int: %i, uint: %u, int: %i, uint: %u, char: %c, %r\n",
            string, positive_integer, negative_integer, unsigned_integer,
            zero_integer, unsigned_zero_integer, character, unknown_format);

    // printf: over!
    const char *print = "printf";
    const char *over = "over";
    printf("%s: %s!\n", print, over);

    uart_tx_disable(&uart);
    while(1);
}

#define SYS_INT_IMPL
#include "sys/int.h"
