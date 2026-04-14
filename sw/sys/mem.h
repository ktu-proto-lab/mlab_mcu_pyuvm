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
extern char __prog_instr_size;
extern char __prog_data_ram_size;
extern char __prog_data_bin_size;

extern char __prog_instr_start;
extern char __prog_instr_end;

extern char __prog_data_start;
extern char __prog_data_end;

extern char __size_text;
extern char __size_data;
extern char __size_bss;
extern char __size_stack;

#define SYSTEM_MEMORY_PROGRAM_INSTR_SIZE_BYTES  ((size_t)&__prog_instr_size)
#define SYSTEM_MEMORY_PROGRAM_RAM_SIZE_BYTES    ((size_t)&__prog_data_ram_size)
#define SYSTEM_MEMORY_PROGRAM_BIN_SIZE_BYTES    ((size_t)&__prog_data_bin_size)

#define SYSTEM_MEMORY_PROGRAM_TEXT_SIZE_BYTES   ((size_t)&__size_text)
#define SYSTEM_MEMORY_PROGRAM_DATA_SIZE_BYTES   ((size_t)&__size_data)
#define SYSTEM_MEMORY_PROGRAM_BSS_SIZE_BYTES    ((size_t)&__size_bss)
#define SYSTEM_MEMORY_PROGRAM_STACK_SIZE_BYTES  ((size_t)&__size_stack)

#endif
