#include "gpio.h"

int main() {
    volatile gpio_handle_t gpio;
    gpio_init(&gpio);
    gpio.regs->OE = GPIO_PIN_0;
    gpio.regs->OUT = GPIO_PIN_0;
    return 0;
}


void __attribute__((interrupt)) GPIO_IRQHandler(void) { while(1); }

void __attribute__((interrupt)) I2C_IRQHandler(void) { while (1); }

void __attribute__((interrupt)) TIMER_IRQHandler(void) { while (1); }

void __attribute__((interrupt)) UART_RX_HALF_FULL_IRQHandler(void) { while (1); }

void __attribute__((interrupt)) UART_TX_HALF_EMPTY_IRQHandler(void) { while (1); }

void __attribute__((interrupt)) UART_RX_NOT_EMPTY_IRQHandler(void) { while (1); }

void __attribute__((interrupt)) UART_TX_NOT_FULL_IRQHandler(void) ;

void UART_TX_NOT_FULL_IRQHandler(void) { while (1); }

void DEFAULT_IRQHandler(void) { while (1); }
