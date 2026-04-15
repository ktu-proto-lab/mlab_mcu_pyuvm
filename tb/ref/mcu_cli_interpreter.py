import shlex
from pyuvm import uvm_object
from errors import NotImplementedError, ConfigError, McuCliWrongCmdStringError
from ref.mcu_memory_mirror import McuMemoryMirror

class McuCliInterpreter(uvm_object):
    def __init__(self, name="McuCli") -> None:
        super().__init__(name)
        self.memory: McuMemoryMirror = None
        self.commands = {
            "echo": self.echo,
            "mem read": self.mem_read,
            "mem write": self.mem_write,
            "mem cksum": self.mem_cksum,
            "mem dump": self.mem_dump,
            "mem size": self.mem_size,
        }

    def execute(self, req: str) -> str:
        if not req:
            raise McuCliWrongCmdStringError()

        if not self.memory:
            raise ConfigError("memory mirror is required")

        if not isinstance(self.memory, McuMemoryMirror):
            raise ConfigError(
                f"memory mirror must be McuMemoryMirror type, actual {type(self.memory).__name__}"
            )

        tokens = shlex.split(req)

        cmd = None
        args = None

        if tokens[0] == "mem" and len(tokens) > 1:
            cmd = f"{tokens[0]} {tokens[1]}"
            args = tokens[2:]

        elif tokens[0] == "echo" and len(tokens) == 2:
            cmd = f"{tokens[0]}"
            args = f"{tokens[1]}"

        if cmd in self.commands:
            return self.commands[cmd](*args)

        return "[  ERROR]: TODO"



    def echo(self, string: str) -> str:
        return string

    def mem_read(self, addr: str) -> str:
        addr: int = int(addr, base=16)
        val = self.memory.read(addr)
        return hex(val)

    def mem_write(self, addr: str, val: str) -> str:
        addr: int = int(addr, base=16)
        val: int = int(val, base=16)
        prev_val: int = self.memory.write(addr, val)
        return hex(prev_val)

    def mem_cksum(self, addr: str, wcnt: str) -> str:
        addr: int = int(addr, base=16)
        wcnt: int = int(wcnt, base=16)
        val: int = self.memory.cksum(addr, wcnt)
        return hex(val)

    def mem_dump(self, addr: str, wcnt: str) -> str:
        addr: int = int(addr, base=16)
        wcnt: int = int(wcnt, base=16)
        vals: list[int] = self.memory.dump(addr, wcnt)
        string = ""
        for val in vals:
            string += f" {hex(val)}"
        return string

    def mem_size(self, type: str) -> str:
        if type == "imem":
            return str(self.memory.IMEM_SIZE_BYTES)

        if type == "dmem":
            return str(self.memory.DMEM_SIZE_BYTES)
        # TODO: implement the rest, maybe use gcc compiler to extract the values of linker variables
        return "TODO"
