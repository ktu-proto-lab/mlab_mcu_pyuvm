#include "lib/string.h"
#include "sys/state.h"
#include "io/printf.h"

bool string_receive(char *buffer, uint32_t lenght) {
    bool string_terminated = false;
    uint32_t count = 0;
    while(count < lenght - 1) {
        uart_receive(&g_uart, (uint8_t *)&buffer[count], sizeof(uint8_t));
        if (buffer[count] == '\n' || buffer[count] == '\0' || buffer[count] == '\r') {
            buffer[count] = '\0';
            system_state_set(SYSTEM_STATE_DEBUG);
            string_terminated = true;
            break;
        }
        count++;
    }

    return string_terminated;
}

int string_compare(const char *lstring, const char *rstring) {
    while(*lstring && (*lstring == *rstring)) {
        lstring++;
        rstring++;
    }

    return *(uint8_t *)lstring - *(uint8_t *)rstring;
}

bool string_hex_to_uint(const char *string, uint32_t *out_value) {
    uint32_t value = 0;

    if (string[0] != '0' || string[1] != 'x') {
        return false;
    }

    string += 2;

    if (*string == '\0') {
        return false;
    }

    while(*string) {
        char c = *string;
        if (c >= '0' && c <= '9') {
            value = (value << 4) | (c - '0');
        } else if (c >= 'a' && c <= 'f') {
            value = (value << 4) | (c - 'a' + 10);
        } else {
            return false;
        }
        ++string;
    }

    *out_value = value;
    return true;
}
