#ifndef LIB_STRING_H
#define LIB_STRING_H

#include <stdbool.h>
#include <stdint.h>

#include "hal/uart.h"

extern uart_handle_t uart;

int string_compare(const char *lstring, const char *rstring);
bool string_receive(char *buffer, uint32_t lenght);

#endif