#include "hal/uart.h"
#include "io/printf.h"

#include <stddef.h>

extern uart_handle_t uart;

static void put_char(const char character) {
    // NOTE: interruptable transmit leads to corrupted printf because of the deallocated stack
    uart_transmit(&uart, (uint8_t *)&character, sizeof(uint8_t));
}

static void print_number(int number, int base, int sign) {
    char buffer[12];
    int i = 0;
    unsigned int unsigned_number;
    
    if (number == 0) {
        put_char('0');
        return;
    }
    
    if (sign && number < 0) {
        put_char('-');
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
        put_char(buffer[i]);
    }
}

static void print_string(const char *string) {
    if (string == NULL) {
        string = "(null)";
    }

    for(; *string != '\0'; ++string) {
        put_char(*string);
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
                    put_char((char)va_arg(args, int));
                    break;
                case 's':
                    print_string(va_arg(args, char *));
                    break;
                case '%':
                    put_char('%');
                    break;
                default:
                    put_char('%');
                    put_char(*format);
                    break;
            }
        } else {
            put_char(*format);
        }
    }

    put_char('\0');

    // clean up the stack (required by C standard)
    va_end(args); 
}