import os
from pyuvm import uvm_object

class McuMemoryConfig(uvm_object):
    def __init__(self, name='McuMemoryConfig'):
        super().__init__(name)
        self.is_set: bool = False
        self.word_size_bytes: int = 4
        self.imem_size_bytes: int = 8192
        self.dmem_size_bytes: int = 4096
        self.imem_base_addr: int = 0x80000000
        self.dmem_base_addr: int = 0x90000000
        self.source_build_dir_path: str = None
        self.imem_file_name: str = "instr_hex.mem"
        self.dmem_file_name: str = "data_hex.mem"
        self.env_sizes_source_filepath: str = None
        self.instr_size_bytes: int = None
        self.ram_size_bytes: int = None
        self.bin_size_bytes: int = None
        self.text_size_bytes: int = None
        self.data_size_bytes: int = None
        self.bss_size_bytes: int = None
        self.stack_size_bytes: int = None
        self.vectors_size_bytes: int = None
        self.nops_size_bytes: int = None
        self.rodata_size_bytes: int = None

    def set(self, filepath: str):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"size export file not found: {filepath}")

        self.env_sizes_source_filepath = filepath

        # NOTE: this parser is very primitive intentionally for failure if some small detail of the env file changes.
        with open(self.env_sizes_source_filepath, "r") as file:

            # /path/to/source_file.elf:
            # section              size         addr
            # .vectors              132   2147483648
            # .text                2580   2147483780
            # .nops                   0   2147486360
            # .rodata               180   2147486360
            # .data                   0   2415919104
            # .bss                   60   2415919104
            # .stack               1024   2415919164
            #
            # from: script/sw_mem_size

            for line in file:
                chunks = line.strip().split()

                if not chunks:
                    continue

                section: str = None
                size: int = None

                if chunks[0].startswith("."):
                    section = chunks[0]
                    size = int(chunks[1])

                if section == ".vectors":
                    self.vectors_size_bytes = size
                elif section == ".text":
                    self.text_size_bytes = size
                elif section == ".nops":
                    self.nops_size_bytes = size
                elif section == ".rodata":
                    self.rodata_size_bytes = size
                elif section == ".data":
                    self.data_size_bytes = size
                elif section == ".bss":
                    self.bss_size_bytes = size
                elif section == ".stack":
                    self.stack_size_bytes = size

        self.instr_size_bytes = self.vectors_size_bytes + self.text_size_bytes + self.nops_size_bytes + self.rodata_size_bytes

        self.ram_size_bytes = self.data_size_bytes + self.bss_size_bytes + self.stack_size_bytes

        self.bin_size_bytes = self.data_size_bytes

        self.is_set = True
