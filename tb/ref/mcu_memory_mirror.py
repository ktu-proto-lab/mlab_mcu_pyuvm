from pyuvm import uvm_object
from errors import MemoryInvalidAddrError, ConfigError

class McuMemoryMirror(uvm_object):
    WORD_SIZE_BYTES: int = 4
    IMEM_SIZE_BYTES: int = 8192
    DMEM_SIZE_BYTES: int = 4096
    IMEM_BASE_ADDR: int = 0x80000000
    DMEM_BASE_ADDR: int = 0x90000000
    DMEM_FILE_NAME: str = "data_hex.mem"
    IMEM_FILE_NAME: str = "instr_hex.mem"

    def __init__(self, name="McuMemoryMirror"):
        super().__init__(name)
        self.source_filepath: string = None
        self.imem: dict = None
        self.dmem: dict = None

    def upload_source_binaries(self):
        if self.source_filepath is None:
            raise ConfigError("source filepath must be set to upload binaries to mcu memory mirror")

        self.imem = self.parse_mem_file(self.source_filepath + self.IMEM_FILE_NAME, self.IMEM_BASE_ADDR)
        self.dmem = self.parse_mem_file(self.source_filepath + self.DMEM_FILE_NAME, self.DMEM_BASE_ADDR)

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
                    addr += self.WORD_SIZE_BYTES

        return mem

    def imem_addr_valid(self, addr: int, bytes: int) -> bool:
        return self.IMEM_BASE_ADDR <= addr and (addr + bytes) <= (self.IMEM_BASE_ADDR + self.IMEM_SIZE_BYTES)

    def dmem_addr_valid(self, addr: int, bytes: int) -> bool:
        return self.DMEM_BASE_ADDR <= (addr + bytes) and (addr + bytes) <= (self.DMEM_BASE_ADDR + self.DMEM_SIZE_BYTES)

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
            cksum ^= self.read(addr + word * self.WORD_SIZE_BYTES)

        return cksum

    def dump(self, addr: int, wcnt: int) -> list[int]:
        vals = []

        for word in range(wcnt):
            word_addr = addr + word * self.WORD_SIZE_BYTES
            word_val = self.read(word_addr)
            vals.append(word_val)

        return vals
