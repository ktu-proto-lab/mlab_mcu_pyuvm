#ifndef SYS_TIME_H
#define SYS_TIME_H

#include <stdint.h>

void time_delay_microseconds(uint64_t duration, uint64_t cpu_freq_mhz);
void time_delay_milliseconds(uint64_t duration, uint64_t cpu_freq_mhz);

#endif
