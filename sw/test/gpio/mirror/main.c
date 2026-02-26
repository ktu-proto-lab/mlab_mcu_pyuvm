#include "main.h"

#include "gpio.c"
#include "irq.c"

volatile gpio_handle_t g_gpio_handle;

int main() {
    gpio_init(&g_gpio_handle);
    g_gpio_handle.regs->oe = GPIO_PIN_0 | GPIO_PIN_1 | GPIO_PIN_2 | GPIO_PIN_3;
    g_gpio_handle.regs->ctrl = GPIO_CTRL_ENA_INT;
    return 0;
}

void gpio_irq_callback(volatile gpio_handle_t *gpio) {
    uint32_t mirror_output;
    mirror_output = (gpio->ints & (GPIO_PIN_4 | GPIO_PIN_5 | GPIO_PIN_6 | GPIO_PIN_7));
    gpio->regs->out = mirror_output >> 4;
}