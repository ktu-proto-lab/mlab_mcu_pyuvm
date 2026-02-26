#include "main.h"

void __attribute__((interrupt)) GPIO_IRQHandler(void) { gpio_irq_handler(&g_gpio_handle); }

void __attribute__((interrupt)) I2C_IRQHandler(void) { while (1); }

void __attribute__((interrupt)) TIMER_IRQHandler(void) { while (1); }

void __attribute__((interrupt)) UART_RX_HALF_FULL_IRQHandler(void) { while (1); }

void __attribute__((interrupt)) UART_TX_HALF_EMPTY_IRQHandler(void) { while (1); }

void __attribute__((interrupt)) UART_RX_NOT_EMPTY_IRQHandler(void) { while (1); }

void __attribute__((interrupt)) UART_TX_NOT_FULL_IRQHandler(void) ;

void UART_TX_NOT_FULL_IRQHandler(void) { while (1); }

void DEFAULT_IRQHandler(void) { while (1); }