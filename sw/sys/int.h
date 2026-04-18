// act as a header file by default
#ifndef SYS_INT_H
#define SYS_INT_H

void __attribute__((interrupt)) GPIO_IRQHandler(void);
void __attribute__((interrupt)) I2C_IRQHandler(void);
void __attribute__((interrupt)) TIMER_IRQHandler(void);
void __attribute__((interrupt)) UART_RX_HALF_FULL_IRQHandler(void);
void __attribute__((interrupt)) UART_TX_HALF_EMPTY_IRQHandler(void);
void __attribute__((interrupt)) UART_RX_NOT_EMPTY_IRQHandler(void);
void __attribute__((interrupt)) UART_TX_NOT_FULL_IRQHandler(void);
void __attribute__((interrupt)) DEFAULT_IRQHandler(void);

#endif

// enforce awareness that 'int.h' is configurable source file from the main.c
#ifdef SYS_INT_IMPL

#include "hal/gpio.h"
#include "hal/uart.h"
#include "sys/glob.h"

#ifdef SYS_INT_GPIO_IRQ_HANDLER_ENABLE
    void GPIO_IRQHandler(void) { gpio_irq_handler(&g_gpio); }
#else
    void __attribute__((weak)) GPIO_IRQHandler(void) {}
#endif

#ifdef SYS_INT_UART_IRQ_HANDLER_ENABLE
    void UART_RX_NOT_EMPTY_IRQHandler(void) { uart_rx_not_empty_irq_handler(&g_uart); }
    void UART_TX_NOT_FULL_IRQHandler(void) { uart_tx_not_full_irq_handler(&g_uart); }
#else
    void __attribute__((weak)) UART_RX_NOT_EMPTY_IRQHandler(void) {}
    void __attribute__((weak)) UART_TX_NOT_FULL_IRQHandler(void) {}
#endif

void __attribute__((weak)) I2C_IRQHandler(void) { while (1); }
void __attribute__((weak)) TIMER_IRQHandler(void) { while (1); }
void __attribute__((weak)) UART_RX_HALF_FULL_IRQHandler(void) { while (1); }
void __attribute__((weak)) UART_TX_HALF_EMPTY_IRQHandler(void) { while (1); }
void __attribute__((weak)) DEFAULT_IRQHandler(void) { while (1); }

#endif
