#include <stdint.h>

#include "hal/gpio.h"
#include "hal/uart.h"
#include "io/cli.h"
#include "io/printf.h"
#include "lib/string.h"
#include "sys/int.h"
#include "sys/time.h"
#include "sys/err.h"
#include "sys/state.h"
#include "sys/mem.h"
#include "sys/glob.h"

static void clear_buffer(char *buffer, uint32_t size) {
    for (uint32_t i = 0; i < size; ++i) {
        buffer[i] = 0;
    }
}

int main() {

    g_init();

    // uart_tx_enable(&uart);
    // // BUG: trying to enable rx like this stalls the test
    // // uart_rx_enable(&uart);

    // // BUG: smaller than 3 chars wide stalls the test, removing does too
    // uart_transmit(&uart, (uint8_t *)"ack\n", 4);

    char buffer[256];
    while (1) {
        system_state_set(&gpio, SYSTEM_STATE_READY);
        // BUG: removing uart_rx/tx_enable stalls test
        uart_rx_enable(&uart);
        string_receive(buffer, sizeof(buffer));
        // BUG: removing with rx enable together
        uart_rx_disable(&uart);
        system_state_set(&gpio, SYSTEM_STATE_BUSY);
        system_error_t e = cli_exec(buffer);
        if (e != SYSTEM_ERROR_NONE) {
            system_error_print(e);
        }
        clear_buffer(buffer, sizeof(buffer));
    }
}

#define SYS_INT_IMPL
#include "sys/int.h"
