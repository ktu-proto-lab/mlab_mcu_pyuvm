#include "sys/err.h"
#include "io/printf.h"

void system_error_print(system_error_t error) {
    printf("[  ERROR]: %u\n", error);
}
