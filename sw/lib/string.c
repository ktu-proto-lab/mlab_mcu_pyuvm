#include "lib/string.h"

bool string_receive(char *buffer, uint32_t lenght) {
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

int string_compare(const char *lstring, const char *rstring) {
    while(*lstring && (*lstring == *rstring)) {
        lstring++;
        rstring++;
    }

    return *(uint8_t *)lstring - *(uint8_t *)rstring;
}
