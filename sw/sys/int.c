#include "sys/int.h"

#include "hal/gpio.h"
#include "hal/uart.h"

#ifdef GPIO_IRQ_HANDLER_ENABLE
    extern volatile gpio_handle_t gpio;
    void GPIO_IRQHandler(void) { gpio_irq_handler(&gpio); }
#else
    void __attribute__((weak)) GPIO_IRQHandler(void) {}
#endif

#ifdef UART_IRQ_HANDLER_ENABLE
    extern volatile uart_handle_t uart;
    void UART_RX_NOT_EMPTY_IRQHandler(void) { uart_rx_not_empty_irq_handler(&uart); }
    void UART_TX_NOT_FULL_IRQHandler(void) { uart_tx_not_full_irq_handler(&uart); }
#else
    void __attribute__((weak)) UART_RX_NOT_EMPTY_IRQHandler(void) {}
    void __attribute__((weak)) UART_TX_NOT_FULL_IRQHandler(void) {}
#endif


void __attribute__((weak)) I2C_IRQHandler(void) { while (1); }
void __attribute__((weak)) TIMER_IRQHandler(void) { while (1); }
void __attribute__((weak)) UART_RX_HALF_FULL_IRQHandler(void) { while (1); }
void __attribute__((weak)) UART_TX_HALF_EMPTY_IRQHandler(void) { while (1); }
void __attribute__((weak)) DEFAULT_IRQHandler(void) { while (1); }
