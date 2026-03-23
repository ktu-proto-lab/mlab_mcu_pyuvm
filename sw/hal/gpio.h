#ifndef HAL_GPIO_H
#define HAL_GPIO_H

#include <stddef.h>
#include <stdint.h>

#include "soc/gpio_regs.h"

typedef struct {
    volatile gpio_reg_map_t *regs;
    uint32_t ints;
} gpio_handle_t;

void gpio_init(volatile gpio_handle_t *gpio);

void gpio_irq_handler(volatile gpio_handle_t *gpio);

void __attribute__((weak)) gpio_irq_callback(volatile gpio_handle_t *gpio);

#endif