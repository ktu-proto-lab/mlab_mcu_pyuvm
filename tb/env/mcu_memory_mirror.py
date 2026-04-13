from pyuvm import uvm_object
from pyuvm.s13_uvm_component import uvm_component
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


    def read(self, addr: int, bytes: int = 0x4) -> int:
        if self.IMEM_BASE_ADDR <= (addr + bytes) and (addr + bytes) <= (self.IMEM_BASE_ADDR + self.IMEM_SIZE_BYTES):
            value: int = 0x0
            for byte in range(bytes):
                value += self.imem[addr + byte] << (byte * 8)
            return value

        if self.DMEM_BASE_ADDR <= (addr + bytes) and (addr + bytes) <= (self.DMEM_BASE_ADDR + self.DMEM_SIZE_BYTES):
            value: int = 0x0
            for byte in range(bytes):
                value += self.dmem[addr + byte] << (byte * 8)
            return value

        raise MemoryInvalidAddrError(
            f"invalid memory address, needs to be in dmem or imem address space, addr={hex(addr)}, bytes={hex(bytes)}"
        )


    def write(self, addr: int, val: int, bytes: int = 0x4) -> None:
        if self.IMEM_BASE_ADDR <= addr and (addr + bytes) <= (self.IMEM_BASE_ADDR + self.IMEM_SIZE_BYTES):
            for byte in range(bytes):
                self.imem[addr + byte] = (val >> (byte * 8)) & 0xFF
            return

        if self.DMEM_BASE_ADDR <= addr and (addr + bytes) <= (self.DMEM_BASE_ADDR + self.DMEM_SIZE_BYTES):
            for byte in range(bytes):
                self.dmem[addr + byte] = (val >> (byte * 8)) & 0xFF
            return

        raise MemoryInvalidAddrError(
            f"invalid memory address, needs to be in dmem or imem address space, addr={hex(addr)}, bytes={hex(bytes)}"
        )

    def cksum(self, addr: int, wcnt: int) -> int:
        cksum: int = 0x0
        for word in range(wcnt):
            cksum ^= self.read(addr + word * self.WORD_SIZE_BYTES)
        return cksum

    def dump(self, addr: int, wcnt: int):
        vals = []
        for word in range(wcnt):
            word_addr = addr + word * self.WORD_SIZE_BYTES
            word_val = self.read(word_addr)
            vals.append(word_val)
        return vals
