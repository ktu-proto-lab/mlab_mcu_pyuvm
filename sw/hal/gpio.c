#include "gpio.h"

void gpio_init(volatile gpio_handle_t *gpio) {
    gpio->regs = (volatile gpio_reg_map_t *)GPIO_BASE_ADDR;
    gpio->regs->IN = 0;
    gpio->regs->OUT = 0;
    gpio->regs->OE = 0;
    gpio->regs->INTE = 0;
    gpio->regs->PTRIG = 0;
    gpio->regs->AUX = 0;
    gpio->regs->CTRL = 0;
    gpio->regs->INTS = 0;

    gpio->ints = 0;
}

void gpio_irq_handler(volatile gpio_handle_t *gpio) {
    gpio->ints = gpio->regs->INTS;
    gpio->regs->INTS = 0;
    gpio_irq_callback(gpio);
}