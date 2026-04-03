#include "hal/gpio.h"
#include "sys/int.h"
#include "soc/gpio_regs.h"

#define GPIO_IRQ_HANDLER_ENABLE
#include "hal/gpio.c"
#include "sys/int.c"

volatile gpio_handle_t gpio;

int main() {
    gpio_init(&gpio);

    gpio.regs->oe = 0xF0;
    gpio.regs->ptrig = 0x0F;
    gpio.regs->ints = 0x0F;
    gpio.regs->inte = 0x0F;
    gpio.regs->ctrl = GPIO_CTRL_ENA_INT;

    while(1);
}

void gpio_irq_callback(volatile gpio_handle_t *gpio) {
    uint32_t current_inputs = (gpio->regs->in & 0x0F);
    gpio->regs->out = current_inputs << 4;
    gpio->regs->ptrig = (~current_inputs) & 0x0F;
    gpio->regs->ints = 0x0F;
}
