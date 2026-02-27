#ifndef GPIO_REGS_H
#define GPIO_REGS_H

#include <stdint.h>

#define GPIO_BASE_ADDR 0x40000000

#define GPIO_PIN_0    ((uint32_t)0x0001)
#define GPIO_PIN_1    ((uint32_t)0x0002)
#define GPIO_PIN_2    ((uint32_t)0x0004)
#define GPIO_PIN_3    ((uint32_t)0x0008)
#define GPIO_PIN_4    ((uint32_t)0x0010)
#define GPIO_PIN_5    ((uint32_t)0x0020)
#define GPIO_PIN_6    ((uint32_t)0x0040)
#define GPIO_PIN_7    ((uint32_t)0x0080)
#define GPIO_PIN_8    ((uint32_t)0x0100)
#define GPIO_PIN_ALL  ((uint32_t)0xFF)

#define GPIO_CTRL_ENA_INT (1 << 0)
#define GPIO_CTRL_GLOBAL_INTS (1 << 1)

typedef struct {
  volatile uint32_t in;
  volatile uint32_t out;
  volatile uint32_t oe;
  volatile uint32_t inte;
  volatile uint32_t ptrig;
  volatile uint32_t aux;
  volatile uint32_t ctrl;
  volatile uint32_t ints;
} gpio_reg_map_t;

#endif