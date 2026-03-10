#ifndef HAL_UART_H
#define HAL_UART_H

#include <stdint.h>

#include "soc/uart_regs.h"

#define UART_BAUD_INTERVAL(cpu_freq_mhz, baudrate) ((cpu_freq_mhz * 1000000) / (baudrate))

#ifndef NULL
#define NULL ((void *)0)
#endif

typedef struct {
    uint32_t baud_rate;
    uint32_t word_length;
    uint32_t stop_bits;
    uint32_t parity;
    uint32_t parity_mode;
    uint32_t parity_lock;
} uart_config_t;

typedef enum {
    UART_STATE_RESET   = 0x00U,
    UART_STATE_READY   = 0x20U,
    UART_STATE_BUSY    = 0x24U,
    UART_STATE_BUSY_TX = 0x21U,
    UART_STATE_BUSY_RX = 0x22U,
    UART_STATE_ERROR   = 0xE0U
} uart_state_t;

typedef struct {
    volatile uart_regs_t *regs;
    uart_config_t config;
    uint8_t *tx_buf;
    uint16_t tx_size;
    volatile uint16_t tx_count;
    uint8_t *rx_buf;
    uint16_t rx_size;
    volatile uint16_t rx_count;
    volatile uart_state_t tx_state;
    volatile uart_state_t rx_state;
} uart_handle_t;

void uart_init(uart_handle_t *uart);
void uart_tx_enable(uart_handle_t *uart);
void uart_tx_disable(uart_handle_t *uart);
void uart_tx_reset(uart_handle_t *uart);
void uart_rx_enable(uart_handle_t *uart);
void uart_rx_disable(uart_handle_t *uart);
void uart_rx_reset(uart_handle_t *uart);

void uart_transmit(uart_handle_t *uart, uint8_t *data, uint16_t size);
void uart_receive(uart_handle_t *uart, uint8_t *data, uint16_t size);
void uart_transmit_it(uart_handle_t *uart, uint8_t *data, uint16_t size);
void uart_receive_it(uart_handle_t *uart, uint8_t *data, uint16_t size);

void uart_rx_not_empty_irq_handler(uart_handle_t *uart);
void uart_tx_not_full_irq_handler(uart_handle_t *uart);

void __attribute__((weak)) uart_rx_cplt_callback(uart_handle_t *uart);
void __attribute__((weak)) uart_tx_cplt_callback(uart_handle_t *uart);

#endif