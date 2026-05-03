import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="vsc")

import vsc
from enum import Enum
from pyuvm import uvm_sequence_item
from errors import CommandUnknownTestError

class CliCmdEnum(Enum):
    read = 1
    write = 2
    cksum = 3
    dump = 4
    test = 5

@vsc.randobj
class CliCmdItem(uvm_sequence_item):
    def __init__(self, name="CliCmd"):
        super().__init__(name)
        self.cmd = vsc.rand_enum_t(CliCmdEnum)
        self.addr = vsc.rand_uint32_t()
        self.value = vsc.rand_uint32_t()
        self.word_count = vsc.rand_uint32_t()


    @vsc.constraint
    def c_mem_addr_space(self):
        imem_base_addr = 0x80000000
        imem_size_bytes = 8192
        dmem_base_addr = 0x90000000
        dmem_size_bytes = 4096
        vsc.dist(self.addr, [
            vsc.weight(vsc.rng(dmem_base_addr, dmem_base_addr + dmem_size_bytes), 50),
            vsc.weight(vsc.rng(imem_base_addr, imem_base_addr + imem_size_bytes), 50)
        ])

    @vsc.constraint
    def c_cmd_write_value_dist(self):
        # check min and max values, and 0
        with vsc.if_then(self.cmd == CliCmdEnum.write):
            int32_t_min_value = -(2**31)
            int32_t_max_value = (2**31) - 1
            vsc.dist(self.value, [
                vsc.weight(0, 5),
                vsc.weight(int32_t_min_value, 5),
                vsc.weight(int32_t_max_value, 5),
                vsc.weight(vsc.rng(1, int32_t_max_value), 30),
                vsc.weight(vsc.rng(int32_t_min_value, -1), 30)
            ])

    @vsc.constraint
    def c_word_count_range(self):
        with vsc.if_then((self.cmd == CliCmdEnum.cksum) | (self.cmd == CliCmdEnum.dump)):
            self.word_count in vsc.rangelist(vsc.rng(1, 16))

    @vsc.constraint
    def c_cmd_equal_dist(self):
        vsc.dist(self.cmd,[
            vsc.weight(CliCmdEnum.read, 30),
            vsc.weight(CliCmdEnum.write, 20),
            vsc.weight(CliCmdEnum.cksum, 20),
            vsc.weight(CliCmdEnum.dump, 20),
            vsc.weight(CliCmdEnum.test, 10)
        ])

    def to_string(self) -> str:
        if self.cmd == CliCmdEnum.read:
            return f"mem read {hex(self.addr)}"
        if self.cmd == CliCmdEnum.write:
            return f"mem write {hex(self.addr)} {hex(self.value)}"
        if self.cmd == CliCmdEnum.cksum:
            return f"mem cksum {hex(self.addr)} {hex(self.word_count)}"
        if self.cmd == CliCmdEnum.dump:
            return f"mem dump {hex(self.addr)} {hex(self.word_count)}"
        if self.cmd == CliCmdEnum.test:
            return "mem test"
        raise CommandUnknownTestError(f"unhandled command {self.cmd}")


    def __str__(self):
        return self.to_string()
