import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="vsc")

import vsc
from enum import Enum
from pyuvm import uvm_sequence_item
from errors import *
from cfg.config import Config

@vsc.randobj
class CliCmdItem(uvm_sequence_item):
    def __init__(self, name="CliCmdItem"):
        super().__init__(name)
        self.cfg: Config = None
        self.cmd: str = None

    def pre_randomize(self):
        if self.cfg is None:
            raise ConfigTestError("configuration must be assigned to the sequence item before randomization")

    def to_string(self):
        raise NotImplementedTestError("method must be implemented by the subclass")

    def __str__(self):
        return self.to_string()

@vsc.randobj
class CliCmdMemItem(CliCmdItem):
    def __init__(self, name='CliCmdMemItem'):
        super().__init__(name)
        self.cmd = "mem"
        self.subcmd: str = None

@vsc.randobj
class CliCmdMemWriteItem(CliCmdMemItem):
    def __init__(self, name="CliCmdMemWriteItem"):
        super().__init__(name)
        self.subcmd = "write"

        self.addr = vsc.rand_uint32_t()
        self.val = vsc.rand_int32_t()

        self.min_addr = vsc.uint32_t()
        self.max_addr = vsc.uint32_t()

        self.min_val = -(2**31)
        self.max_val = (2**31) - 1

    def pre_randomize(self):
        super().pre_randomize()
        self.min_addr = self.cfg.mem_cfg.imem_base_addr + self.cfg.mem_cfg.instr_size_bytes
        self.max_addr = self.cfg.mem_cfg.imem_base_addr + self.cfg.mem_cfg.imem_size_bytes - self.cfg.mem_cfg.word_size_bytes

    @vsc.constraint
    def c_addr_space(self):
        self.addr >= self.min_addr
        self.addr <= self.max_addr

    @vsc.constraint
    def c_val_dist(self):
        vsc.dist(self.val,[
            vsc.weight(vsc.rng(self.min_val, -1), 10),
            vsc.weight(vsc.rng(0, self.max_val), 90)
        ])

    def to_string(self):
        return f"{self.cmd} {self.subcmd} {hex(self.addr)} {hex(self.val & 0xFFFFFFFF)}"
