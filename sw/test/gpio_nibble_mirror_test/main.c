#include "hal/gpio.h"
#include "sys/int.h"
#include "sys/glob.h"

int main() {
    gpio_init(&g_gpio);
    g_gpio.regs->oe = 0xF0;
    g_gpio.regs->ptrig = 0x0F;
    g_gpio.regs->inte = 0x0F;
    g_gpio.regs->ctrl = GPIO_CTRL_ENA_INT;
    // g_gpio.regs->out = SYSTEM_STATE_DEBUG;
    while(1);
}

void gpio_irq_callback(volatile gpio_handle_t *gpio) {
    uint32_t current_inputs = (gpio->regs->in & 0x0F);
    gpio->regs->out = current_inputs << 4;
    gpio->regs->ptrig = (~current_inputs) & 0x0F;
}

#define SYS_INT_IMPL
#define SYS_INT_GPIO_IRQ_HANDLER_ENABLE
#include "sys/int.h"
