#include "uart.h"

void uart_init(uart_handle_t *uart) {
    uart->regs = (volatile uart_regs_t *)UART_BASE_ADDR;

    if (uart->tx_state == UART_STATE_RESET) {

        uart->regs->setup = ((uart->config.baud_rate << 0) & UART_SETUP_BAUD_MASK)
                          | (uart->config.parity_mode << 24)
                          | (uart->config.parity_lock << 25)
                          | (uart->config.parity      << 26)
                          | (uart->config.stop_bits    << 27)
                          | (uart->config.word_length  << 28);

        uart->tx_state = UART_STATE_READY;
        uart->rx_state = UART_STATE_READY;
    }
}

void uart_tx_enable(uart_handle_t *uart) {
    if (uart->tx_state == UART_STATE_READY) {
        uart->regs->control |= UART_CTRL_TX_EN;
    }
}

void uart_tx_disable(uart_handle_t *uart) {
    if (uart->tx_state == UART_STATE_READY) {
        uart->regs->control &= ~UART_CTRL_TX_EN;
    }
}

void uart_tx_reset(uart_handle_t *uart) {
    uart->regs->control |= UART_CTRL_TX_RST;
}

void uart_rx_enable(uart_handle_t *uart) {
    if (uart->rx_state == UART_STATE_READY) {
        uart->regs->control |= UART_CTRL_RX_EN;
    }
}

void uart_rx_disable(uart_handle_t *uart) {
    if (uart->rx_state == UART_STATE_READY) {
        uart->regs->control &= ~UART_CTRL_RX_EN;
    }
}

void uart_rx_reset(uart_handle_t *uart) {
    uart->regs->control |= UART_CTRL_RX_RST;
}

void uart_transmit(uart_handle_t *uart, uint8_t *data, uint16_t size) {
    if (uart->tx_state != UART_STATE_READY || data == NULL || size == 0) {
        return;
    }

    while (size > 0) {
        if (!(uart->regs->tx_data & UART_TX_BUSY)) {
            uart->regs->tx_data = *data;
            data++;
            size--;
        }
    }
    while (uart->regs->tx_data & UART_TX_BUSY);
}

void uart_receive(uart_handle_t *uart, uint8_t *data, uint16_t size) {
    while (size > 0) {
        uint32_t rx_data = uart->regs->rx_data;
        if (rx_data & UART_RX_EMPTY) {
            *data++ = (uint8_t)(rx_data & 0xFF);
            size--;
        }
    }
}

void uart_transmit_it(uart_handle_t *uart, uint8_t *data, uint16_t size) {
    if (uart->tx_state != UART_STATE_READY || data == NULL || size == 0) {
        return;
    }

    uart->tx_buf = data;
    uart->tx_size = size;
    uart->tx_count = size;
    uart->tx_state = UART_STATE_BUSY_TX;

    uart->regs->control |= UART_CTRL_TX_INT_EN;
}

void uart_receive_it(uart_handle_t *uart, uint8_t *data, uint16_t size) {
    if (uart->rx_state != UART_STATE_READY || data == NULL || size == 0) {
        return;
    }

    uart->rx_buf = data;
    uart->rx_size = size;
    uart->rx_count = size;
    uart->rx_state = UART_STATE_BUSY_RX;

    uart->regs->control |= UART_CTRL_RX_INT_EN;
}

void uart_rx_not_empty_irq_handler(uart_handle_t *uart) {
    if (uart->rx_state == UART_STATE_BUSY_RX) {
        *(uart->rx_buf) = (uint8_t)(uart->regs->rx_data & 0xFF);
        uart->rx_buf++;
        uart->rx_count--;

        if (uart->rx_count == 0) {
            uart->regs->control &= ~UART_CTRL_RX_INT_EN;
            uart->rx_state = UART_STATE_READY;
            if (uart_rx_cplt_callback != NULL) {
                uart_rx_cplt_callback(uart);
            }
        }
    }
}

void uart_tx_not_full_irq_handler(uart_handle_t *uart) {
    if (uart->tx_state == UART_STATE_BUSY_TX) {
        if (uart->tx_count == 0) {
            uart->regs->control &= ~UART_CTRL_TX_INT_EN;
            uart->tx_state = UART_STATE_READY;
            if (uart_tx_cplt_callback != NULL) {
                uart_tx_cplt_callback(uart);
            }
        } else {
            uart->regs->tx_data = *(uart->tx_buf);
            uart->tx_buf++;
            uart->tx_count--;
        }
    }
}
