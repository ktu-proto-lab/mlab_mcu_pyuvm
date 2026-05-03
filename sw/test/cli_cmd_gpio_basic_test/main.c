#define SYS_INT_IMPL

#include "sys/glob.h"
#include "sys/int.h"

int main() {
    g_init();
    g_gpio.regs->oe = 0xFF;
    while(1) {
        g_gpio.regs->out = 0xFF;
    }
}