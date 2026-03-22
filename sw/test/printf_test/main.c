#include <stdint.h>
#include <stdarg.h>

#include "hal/gpio.c"
#include "hal/uart.c"
#include "sys/int.c"

uart_handle_t uart;
gpio_handle_t gpio;

static void uart_put_char(const char character) {
    uart_transmit(&uart, (uint8_t *)&character, sizeof(uint8_t));
}

static void print_number(int number, int base, int sign) {
    char buffer[12];
    int i = 0;
    unsigned int unsigned_number;
    
    if (number == 0) {
        uart_put_char('0');
        return;
    }
    
    if (sign && number < 0) {
        uart_put_char('-');
        unsigned_number = (unsigned int)(~number + 1);
    } else {
        unsigned_number = (unsigned int)number;
    }

    for (; unsigned_number > 0; ++i) {
        unsigned int remainder = unsigned_number % base;

        if (remainder < 10) {
            buffer[i] = remainder + '0';
        } else {
            buffer[i] = remainder - 10 + 'a';
        }
        
        unsigned_number /= base;
    }

    while (i > 0) {
        --i;
        uart_put_char(buffer[i]);
    }
}

static void print_string(const char *string) {
    if (string == NULL) {
        string = "(null)";
    }

    for(; *string != '\0'; ++string) {
        uart_put_char(*string);
    }
}

void printf(const char *format, ...) {
    va_list args;
    va_start(args, format);

    for (; *format != '\0'; ++format) {
        if (*format == '%') {
            format++;

            switch(*format) {
                case 'i':
                    print_number(va_arg(args, int), 10, 1);
                    break;
                case 'u':
                    print_number(va_arg(args, unsigned int), 10, 0);
                    break;
                case 'x':
                    print_number(va_arg(args, unsigned int), 16, 0);
                    break;
                case 'c':
                    uart_put_char((char)va_arg(args, int));
                    break;
                case 's':
                    print_string(va_arg(args, char *));
                    break;
                case '%':
                    uart_put_char('%');
                    break;
                default:
                    uart_put_char('%');
                    uart_put_char(*format);
                    break;
            }
        } else {
            uart_put_char(*format);
        }
    }
    
    // add null termination at the end
    uart_put_char(*format);

    // clean up the stack (required by C standard)
    va_end(args); 
}

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

    // printf: s: string, int: 189, int: -9021, uint: 1926478, int: 0, uint: 0, char: h, %r\x00
    const char *string = "string";
    const int positive_integer = 189;
    const int negative_integer = -9021;
    const unsigned int unsigned_integer = 1926478;
    const int zero_integer = 0;
    const unsigned int unsigned_zero_integer = 0;
    const char character = 'h';
    const char *unknown_format = "fmt";
    printf("printf: s: %s, int: %i, int: %i, uint: %u, int: %i, uint: %u, char: %c, %r",
            string, positive_integer, negative_integer, unsigned_integer,
            zero_integer, unsigned_zero_integer, character, unknown_format);

    // printf: over!\x00
    const char *print = "printf";
    const char *over = "over";
    printf("%s: %s!", print, over);

    uart_tx_disable(&uart);
    while(1);
}
