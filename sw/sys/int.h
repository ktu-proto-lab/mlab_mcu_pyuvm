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
