#ifndef SYS_STATE_H
#define SYS_STATE_H

#include <stdint.h>

#include "hal/gpio.h"

typedef enum {
    SYSTEM_STATE_READY  = 0b10000000,
    SYSTEM_STATE_BUSY   = 0b01000000,
    SYSTEM_STATE_DEBUG  = 0b00100000,
    SYSTEM_STATE_MASK   = 0b11100000,
} system_state_t;

inline void system_state_set(gpio_handle_t *gpio, system_state_t state) {
    gpio->regs->out = (gpio->regs->out & ~SYSTEM_STATE_MASK) | state;
}

#endif
