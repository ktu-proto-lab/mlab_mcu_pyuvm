#ifndef SYS_GLOB_H
#define SYS_GLOB_H

#include "hal/gpio.h"
#include "hal/uart.h"
#include "sys/state.h"

extern volatile gpio_handle_t g_gpio;
extern volatile uart_handle_t g_uart;
extern const uint32_t g_cpu_freq_mhz;
extern const uint32_t g_uart_baud_rate;

void g_init(void);

#endif
