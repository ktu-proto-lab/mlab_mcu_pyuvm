#ifndef SOC_UART_REGS_H
#define SOC_UART_REGS_H

#define UART_BASE_ADDR 0x50000000

#define UART_SETUP_N (1 << 28)
#define UART_SETUP_S (1 << 27)
#define UART_SETUP_P (1 << 26)
#define UART_SETUP_F (1 << 25)
#define UART_SETUP_T (1 << 24)
#define UART_SETUP_BAUD (1 << 0)
#define UART_SETUP_BAUD_MASK 0xFFFFFF

#define UART_CTRL_TX_RST (1 << 5)
#define UART_CTRL_TX_INT_EN (1 << 4)
#define UART_CTRL_TX_EN (1 << 3)
#define UART_CTRL_RX_RST (1 << 2)
#define UART_CTRL_RX_INT_EN (1 << 1)
#define UART_CTRL_RX_EN (1 << 0)

#define UART_RX_C (1 << 13)
#define UART_RX_BREAK (1 << 12)
#define UART_RX_ERR (1 << 11)
#define UART_RX_FRAME_ERR (1 << 10)
#define UART_RX_PARITY_ERR (1 << 9)
#define UART_RX_EMPTY (1 << 8)
#define UART_RX_BYTE_WIDTH 8
#define UART_RX_BYTE (1 << 0)

#define UART_TX_O (1 << 11)
#define UART_TX_BREAK (1 << 10)
#define UART_TX_BUSY (1 << 9)
#define UART_TX_EMPTY (1 << 8)
#define UART_TX_BYTE_WIDTH 8
#define UART_TX_BYTE (1 << 0)

typedef struct {
    volatile uint32_t setup;   
    volatile uint32_t control; 
    volatile uint32_t rx_data; 
    volatile uint32_t tx_data; 
} uart_regs_t;

#endif
