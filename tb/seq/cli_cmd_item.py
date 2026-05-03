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

@vsc.randobj
class CliCmdMemReadItem(CliCmdMemItem):
    def __init__(self, name='CliCmdMemItem'):
        super().__init__(name)
        self.subcmd = "read"

        self.addr = self.addr = vsc.rand_uint32_t()

        self.imem_min_addr = vsc.uint32_t()
        self.imem_max_addr = vsc.uint32_t()
        self.dmem_min_addr = vsc.uint32_t()
        self.dmem_max_addr = vsc.uint32_t()

    def pre_randomize(self):
        super().pre_randomize()
        self.imem_min_addr = self.cfg.mem_cfg.imem_base_addr
        self.imem_max_addr = self.cfg.mem_cfg.imem_base_addr + self.cfg.mem_cfg.imem_size_bytes - self.cfg.mem_cfg.word_size_bytes
        self.dmem_min_addr = self.cfg.mem_cfg.dmem_base_addr
        self.dmem_max_addr = self.cfg.mem_cfg.dmem_base_addr + self.cfg.mem_cfg.dmem_size_bytes - self.cfg.mem_cfg.word_size_bytes

    @vsc.constraint
    def c_addr_space(self):
        # TODO: favor the stack and bss in dmem and instructions in imem for better checkup
        (
            ((self.addr >= self.imem_min_addr) & (self.addr <= self.imem_max_addr))
            |
            ((self.addr >= self.dmem_min_addr) & (self.addr <= self.dmem_max_addr))
        )

    def to_string(self):
        return f"{self.cmd} {self.subcmd} {hex(self.addr)}"

@vsc.randobj
class CliCmdMemDumpItem(CliCmdMemItem):
    def __init__(self, name='CliCmdMemDumpItem'):
        super().__init__(name)
        self.subcmd = "dump"

        self.addr = vsc.rand_uint32_t()
        self.word_count = vsc.rand_uint32_t()

        self.imem_min_addr = vsc.uint32_t()
        self.imem_max_addr = vsc.uint32_t()
        self.dmem_min_addr = vsc.uint32_t()
        self.dmem_max_addr = vsc.uint32_t()

        self.word_size_bytes = vsc.uint32_t()

        self.min_word_count = 1
        self.max_word_count = 16

    def pre_randomize(self):
        super().pre_randomize()
        self.word_size_bytes = self.cfg.mem_cfg.word_size_bytes

        self.imem_min_addr = self.cfg.mem_cfg.imem_base_addr
        self.imem_max_addr = self.cfg.mem_cfg.imem_base_addr + self.cfg.mem_cfg.imem_size_bytes - self.word_size_bytes

        self.dmem_min_addr = self.cfg.mem_cfg.dmem_base_addr
        self.dmem_max_addr = self.cfg.mem_cfg.dmem_base_addr + self.cfg.mem_cfg.dmem_size_bytes - self.word_size_bytes

    @vsc.constraint
    def c_word_count(self):
        self.word_count >= self.min_word_count
        self.word_count <= self.max_word_count

    @vsc.constraint
    def c_addr_space(self):
        (
            (
                (self.addr >= self.imem_min_addr) &
                ((self.addr + (self.word_count - 1) * self.word_size_bytes) <= self.imem_max_addr)
            )
            |
            (
                (self.addr >= self.dmem_min_addr) &
                ((self.addr + (self.word_count - 1) * self.word_size_bytes) <= self.dmem_max_addr)
            )
        )

    def to_string(self):
        return f"{self.cmd} {self.subcmd} {hex(self.addr)} {hex(self.word_count)}"

@vsc.randobj
class CliCmdMemCksumItem(CliCmdMemItem):
    def __init__(self, name='CliCmdMemCksumItem'):
        super().__init__(name)
        self.subcmd = "cksum"

        self.addr = vsc.rand_uint32_t()
        self.word_count = vsc.rand_uint32_t()

        self.imem_min_addr = vsc.uint32_t()
        self.imem_max_addr = vsc.uint32_t()
        self.dmem_min_addr = vsc.uint32_t()
        self.dmem_max_addr = vsc.uint32_t()

        self.word_size_bytes = vsc.uint32_t()

        self.min_word_count = 1
        self.max_word_count = 16

    def pre_randomize(self):
        super().pre_randomize()
        self.word_size_bytes = self.cfg.mem_cfg.word_size_bytes

        self.imem_min_addr = self.cfg.mem_cfg.imem_base_addr
        self.imem_max_addr = self.cfg.mem_cfg.imem_base_addr + self.cfg.mem_cfg.imem_size_bytes - self.word_size_bytes

        self.dmem_min_addr = self.cfg.mem_cfg.dmem_base_addr
        self.dmem_max_addr = self.cfg.mem_cfg.dmem_base_addr + self.cfg.mem_cfg.dmem_size_bytes - self.word_size_bytes

    @vsc.constraint
    def c_word_count(self):
        self.word_count >= self.min_word_count
        self.word_count <= self.max_word_count

    @vsc.constraint
    def c_addr_space(self):
        (
            (
                (self.addr >= self.imem_min_addr) &
                ((self.addr + (self.word_count - 1) * self.word_size_bytes) <= self.imem_max_addr)
            )
            |
            (
                (self.addr >= self.dmem_min_addr) &
                ((self.addr + (self.word_count - 1) * self.word_size_bytes) <= self.dmem_max_addr)
            )
        )

    def to_string(self):
        return f"{self.cmd} {self.subcmd} {hex(self.addr)} {hex(self.word_count)}"

@vsc.randobj
class CliCmdMemTestItem(CliCmdMemItem):
    def __init__(self, name='CliCmdMemTestItem'):
        super().__init__(name)
        self.subcmd = "test"

    def to_string(self):
        return f"{self.cmd} {self.subcmd}"

@vsc.randobj
class CliCmdGpioItem(CliCmdItem):
    def __init__(self, name="CliCmdGpioItem"):
        super().__init__(name)
        self.cmd = "gpio"
        self.subcmd: str = None

@vsc.randobj
class CliCmdGpioGetItem(CliCmdGpioItem):
    def __init__(self, name="CliCmdGpioGetItem"):
        super().__init__(name)
        self.subcmd = "get"

        self.has_pin_arg = vsc.rand_bit_t(1)
        self.pin_count = vsc.uint32_t()
        self.big_pin = vsc.uint32_t()
        self.little_pin = vsc.uint32_t()
        self.pin = vsc.rand_uint32_t()

    def pre_randomize(self):
        super().pre_randomize()
        self.pin_count = self.cfg.gpio_cfg.pin_count
        self.big_pin = self.pin_count - 1
        self.little_pin = 0

    @vsc.constraint
    def c_pin_range(self):
        self.pin >= self.little_pin
        self.pin <= self.big_pin

    def to_string(self):
        if self.has_pin_arg:
            return f"{self.cmd} {self.subcmd} {hex(self.pin)}"
        return f"{self.cmd} {self.subcmd}"
