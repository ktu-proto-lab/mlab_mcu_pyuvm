#include "sys/time.h"

void time_delay_microseconds(uint64_t duration, uint64_t cpu_freq_mhz) {
    uint64_t curr_cycle;
    uint32_t mcycle;
    uint32_t mcycleh;

    uint64_t total_wait_cycles = duration * cpu_freq_mhz;

    __asm__ volatile ("csrr %0, mcycle" : "=r"(mcycle));
    __asm__ volatile ("csrr %0, mcycleh" : "=r"(mcycleh));
    curr_cycle = (uint64_t)mcycle | ((uint64_t)mcycleh << 32);

    total_wait_cycles += curr_cycle;

    while (curr_cycle < total_wait_cycles) {
        __asm__ volatile ("csrr %0, mcycle" : "=r"(mcycle));
        __asm__ volatile ("csrr %0, mcycleh" : "=r"(mcycleh));
        curr_cycle = (uint64_t)mcycle | ((uint64_t)mcycleh << 32);
    }
}

void time_delay_milliseconds(uint64_t duration, uint64_t cpu_freq_mhz) {
    time_delay_microseconds(duration * 1000, cpu_freq_mhz);
}
