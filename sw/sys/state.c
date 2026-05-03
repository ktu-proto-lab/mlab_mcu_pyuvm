#include "sys/state.h"
#include "sys/glob.h"

void system_state_set(system_state_t state) {
    g_gpio.regs->out = (g_gpio.regs->out & ~SYSTEM_STATE_MASK) | state;
}