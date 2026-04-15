#ifndef LIB_STRING_H
#define LIB_STRING_H

#include <stdbool.h>
#include <stdint.h>

#include "sys/glob.h"

int string_compare(const char *lstring, const char *rstring);
bool string_receive(char *buffer, uint32_t lenght);
bool string_hex_to_uint(const char *string, uint32_t *out_value);

#endif
