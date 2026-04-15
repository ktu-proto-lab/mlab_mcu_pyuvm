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

    char buffer[256];
    while (1) {
        system_state_set(&g_gpio, SYSTEM_STATE_READY);
        // BUG: removing uart_rx/tx_enable stalls test
        uart_rx_enable(&g_uart);
        string_receive(buffer, sizeof(buffer));
        // BUG: removing with rx enable together
        uart_rx_disable(&g_uart);
        system_state_set(&g_gpio, SYSTEM_STATE_BUSY);
        system_error_t e = cli_exec(buffer);
        if (e != SYSTEM_ERROR_NONE) {
            system_error_print(e);
        }
        clear_buffer(buffer, sizeof(buffer));
    }
}

// heads up for mr. Zozin
#define SYS_INT_IMPL
#include "sys/int.h"
