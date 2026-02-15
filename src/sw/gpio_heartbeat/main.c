#include <stdint.h>

#define GPIO_ADDR 0x40000000

volatile uint32_t g_gpio_int_status = 0;

int main() {
    volatile uint32_t* gpio_regs;
    gpio_regs = (uint32_t*) GPIO_ADDR;

    *(gpio_regs + 6) = 0x01;
    *(gpio_regs + 3) = 0x08;

    while(1){
        if(g_gpio_int_status == 0x8) {  // interrupt on GPIO_PIN_3
            g_gpio_int_status = 0;
            *(gpio_regs + 1) = 0x1;     // toggle GPIO_PIN_0
        }
    }
}

void gpio_handler(void){
    volatile uint32_t* reg;
    reg = (uint32_t*) (GPIO_ADDR + 0x1C);
    g_gpio_int_status = *reg;
    *reg = 0x0;
}

void __attribute__((interrupt)) GPIO_IRQHandler(void) { gpio_handler(); }

void __attribute__((interrupt)) I2C_IRQHandler(void) { while (1); }

void __attribute__((interrupt)) TIMER_IRQHandler(void) { while (1); }

void __attribute__((interrupt)) UART_RX_HALF_FULL_IRQHandler(void) { while (1); }

void __attribute__((interrupt)) UART_TX_HALF_EMPTY_IRQHandler(void) { while (1); }

void __attribute__((interrupt)) UART_RX_NOT_EMPTY_IRQHandler(void) { while (1); }

void __attribute__((interrupt)) UART_TX_NOT_FULL_IRQHandler(void) ;

void UART_TX_NOT_FULL_IRQHandler(void) { while (1); }

void DEFAULT_IRQHandler(void) { while (1); }
