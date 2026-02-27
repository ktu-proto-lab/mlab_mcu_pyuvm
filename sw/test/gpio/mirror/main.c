#include "main.h"
#include "gpio.c"
#include "irq.c"

volatile gpio_handle_t g_gpio_handle;

int main() {
    gpio_init(&g_gpio_handle);
    
    g_gpio_handle.regs->oe = 0xF0;
    g_gpio_handle.regs->ptrig = 0x0F;
    g_gpio_handle.regs->ints = 0x0F; 
    g_gpio_handle.regs->inte = 0x0F;
    g_gpio_handle.regs->ctrl = GPIO_CTRL_ENA_INT;

    while(1);
}

void gpio_irq_callback(volatile gpio_handle_t *gpio) {
    uint32_t current_inputs = (gpio->regs->in & 0x0F);
    gpio->regs->out = current_inputs << 4;
    gpio->regs->ptrig = (~current_inputs) & 0x0F;
    gpio->regs->ints = 0x0F;
}