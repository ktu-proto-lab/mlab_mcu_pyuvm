#include "gpio.h"

void gpio_init(volatile gpio_handle_t *gpio) {
    gpio->regs = (volatile gpio_reg_map_t *)GPIO_BASE_ADDR;
    gpio->regs->in = 0;
    gpio->regs->out = 0;
    gpio->regs->oe = 0;
    gpio->regs->inte = 0;
    gpio->regs->ptrig = 0;
    gpio->regs->aux = 0;
    gpio->regs->ctrl = 0;
    gpio->regs->ints = 0;

    gpio->ints = 0;
}

void gpio_irq_handler(volatile gpio_handle_t *gpio) {
    gpio->ints = gpio->regs->ints;
    gpio->regs->ints = 0;

    if (gpio_irq_callback != NULL) {
        gpio_irq_callback(gpio);
    }
}
