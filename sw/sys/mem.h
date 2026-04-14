#ifndef SYS_MEM_H
#define SYS_MEM_H

#define SYSTEM_MEMORY_IMEM_BASE_ADDR 0x80000000UL
#define SYSTEM_MEMORY_DMEM_BASE_ADDR 0x90000000UL

#define SYSTEM_MEMORY_IMEM_SIZE 8192UL
#define SYSTEM_MEMORY_DMEM_SIZE 4096UL

#define SYSTEM_MEMORY_WORD_SIZE_BYTES 4UL

#define SYSTEM_MEMORY_IMEM_ADDR_VALID(a) \
    ((a) >= SYSTEM_MEMORY_IMEM_BASE_ADDR && \
     (a) <= (SYSTEM_MEMORY_IMEM_BASE_ADDR + SYSTEM_MEMORY_IMEM_SIZE - 4))

#define SYSTEM_MEMORY_DMEM_ADDR_VALID(a) \
    ((a) >= SYSTEM_MEMORY_DMEM_BASE_ADDR && \
     (a) <= (SYSTEM_MEMORY_DMEM_BASE_ADDR + SYSTEM_MEMORY_DMEM_SIZE - 4))

#define SYSTEM_MEMORY_ADDR_VALID(a) \
    (SYSTEM_MEMORY_IMEM_ADDR_VALID(a) || SYSTEM_MEMORY_DMEM_ADDR_VALID(a))

// Defined by the linker, look in root/sw/ibex/common/link.ld (PATCH 4)
extern char __imem_size;
extern char __dmem_size_ram;
extern char __dmem_size_bin;

#define SYSTEM_MEMORY_PROGRAM_TEXT_SIZE_BYTES (size_t)&__imem_size
#define SYSTEM_MEMORY_PROGRAM_DATA_SIZE_BYTES (size_t)&__dmem_size_ram
#define SYSTEM_MEMORY_PROGRAM_BSS_SIZE_BYTES (size_t)&__dmem_size_bin

#endif
