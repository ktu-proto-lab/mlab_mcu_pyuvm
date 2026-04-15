from pyuvm import uvm_object
from errors import MemoryInvalidAddrError, ConfigError
from env.mcu_memory_config import McuMemoryConfig

class McuMemoryMirror(uvm_object):
    def __init__(self, name="McuMemoryMirror"):
        super().__init__(name)
        self.cfg: McuMemoryConfig = None
        self.imem: dict = None
        self.dmem: dict = None

    def upload_source_binaries(self):
        if self.cfg is None:
            raise ConfigError(
                "memory configuration must be set to upload binaries to mcu memory mirror"
            )

        if not isinstance(self.cfg, McuMemoryConfig):
            raise ConfigError(
                f"memory configuration expected to be McuMemoryConfig, actual is {type(self.cfg).__name__}"
            )

        self.imem = self.parse_mem_file(self.cfg.source_build_dir_path + self.cfg.imem_file_name, self.cfg.imem_base_addr)
        self.dmem = self.parse_mem_file(self.cfg.source_build_dir_path + self.cfg.dmem_file_name, self.cfg.dmem_base_addr)

    def parse_mem_file(self, filepath: str, base_addr: int) -> dict:
        mem = {}

        with open(filepath, "r") as file:
            addr = base_addr

            for line in file:
                line = line.strip()

                if not line or line.startswith("@"):
                    continue

                for word_str in line.split():
                    word = int(word_str, 16)
                    mem[addr + 0] = (word >> 0)  & 0xFF
                    mem[addr + 1] = (word >> 8)  & 0xFF
                    mem[addr + 2] = (word >> 16) & 0xFF
                    mem[addr + 3] = (word >> 24) & 0xFF
                    addr += self.cfg.word_size_bytes

        return mem

    def imem_addr_valid(self, addr: int, bytes: int) -> bool:
        return self.cfg.imem_base_addr <= addr and (addr + bytes) <= (self.cfg.imem_base_addr + self.cfg.imem_size_bytes)

    def dmem_addr_valid(self, addr: int, bytes: int) -> bool:
        return self.cfg.dmem_base_addr <= (addr + bytes) and (addr + bytes) <= (self.cfg.dmem_base_addr + self.cfg.dmem_size_bytes)

    def addr_valid(self, addr: int, bytes: int) -> bool:
        return self.imem_addr_valid(addr, bytes) or self.dmem_addr_valid(addr, bytes)

    def read(self, addr: int, bytes: int = 0x4) -> int:
        if not self.addr_valid(addr, bytes):
            raise MemoryInvalidAddrError(
                f"invalid memory read address, needs to be in dmem or imem address space, addr={hex(addr)}, bytes={hex(bytes)}"
            )

        mem = None

        if self.imem_addr_valid(addr, bytes):
            mem = self.imem

        elif self.dmem_addr_valid(addr, bytes):
            mem = self.dmem

        value: int = 0x0

        for byte in range(bytes):
            value += mem[addr + byte] << (byte * 8)

        return value

    def write(self, addr: int, val: int, bytes: int = 0x4) -> None:
        if not self.addr_valid(addr, bytes):
            raise MemoryInvalidAddrError(
                f"invalid memory write address, needs to be in dmem or imem address space, addr={hex(addr)}, bytes={hex(bytes)}"
            )

        mem = None

        if self.imem_addr_valid(addr, bytes):
            mem = self.imem

        elif self.dmem_addr_valid(addr, bytes):
            mem = self.dmem

        prev_val: int = self.read(addr, bytes)

        for byte in range(bytes):
            mem[addr + byte] = (val >> (byte * 8)) & 0xFF

        return prev_val

    def cksum(self, addr: int, wcnt: int) -> int:
        cksum: int = 0x0

        for word in range(wcnt):
            cksum ^= self.read(addr + word * self.cfg.word_size_bytes)

        return cksum

    def dump(self, addr: int, wcnt: int) -> list[int]:
        vals = []

        for word in range(wcnt):
            word_addr = addr + word * self.cfg.word_size_bytes
            word_val = self.read(word_addr)
            vals.append(word_val)

        return vals
