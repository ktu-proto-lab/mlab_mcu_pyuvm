#include <stdint.h>

#define GPIO_BASE_ADDR 0x40000000

typedef struct {
  volatile uint32_t IN;
  volatile uint32_t OUT;
  volatile uint32_t OE;
  volatile uint32_t INTE;
  volatile uint32_t PTRIG;
  volatile uint32_t AUX;
  volatile uint32_t CTRL;
  volatile uint32_t INTS;
} GPIO_reg_map_t;

#define GPIO_PIN_0 ((uint32_t)0x0001)
#define GPIO_PIN_1 ((uint32_t)0x0002)
#define GPIO_PIN_2 ((uint32_t)0x0004)
#define GPIO_PIN_3 ((uint32_t)0x0008)
#define GPIO_PIN_4 ((uint32_t)0x0010)
#define GPIO_PIN_5 ((uint32_t)0x0020)
#define GPIO_PIN_6 ((uint32_t)0x0040)
#define GPIO_PIN_7 ((uint32_t)0x0080)
#define GPIO_PIN_8 ((uint32_t)0x0100)
#define GPIO_PIN_9 ((uint32_t)0x0200)
#define GPIO_PIN_10 ((uint32_t)0x0400)
#define GPIO_PIN_11 ((uint32_t)0x0800)

#define GPIO_CTRL_EN_INT (1 << 0)