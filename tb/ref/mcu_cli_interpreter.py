import shlex
from pyuvm import uvm_object
from errors import NotImplementedTestError, ConfigTestError, McuCliWrongCmdStringTestError, McuCliCmdNotExacutableTestError

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
            "mem test": self.mem_test,
        }

    def execute(self, req: str) -> str:
        if not req:
            raise McuCliWrongCmdStringTestError()

        if not self.memory:
            raise ConfigTestError("memory mirror is required")

        if not isinstance(self.memory, McuMemoryMirror):
            raise ConfigTestError(
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

        raise McuCliCmdNotExacutableTestError(
            f"given request can not be executed by the interpreter '{req}'"
        )

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
            string += f"{hex(val)} "
        return string

    def mem_size(self, type: str) -> str:
        if type == "imem":
            return str(self.memory.cfg.imem_size_bytes)
        if type == "dmem":
            return str(self.memory.cfg.dmem_size_bytes)
        if type == "instr":
            return str(self.memory.cfg.instr_size_bytes)
        if type == "ram":
            return str(self.memory.cfg.ram_size_bytes)
        if type == "bin":
            return str(self.memory.cfg.bin_size_bytes)
        if type == "text":
            return str(self.memory.cfg.text_size_bytes)
        if type == "data":
            return str(self.memory.cfg.data_size_bytes)
        if type == "bss":
            return str(self.memory.cfg.bss_size_bytes)
        if type == "stack":
            return str(self.memory.cfg.stack_size_bytes)

        SYSTEM_ERROR_CLI_CMD_MEM_SIZE_UNKNOWN_ARG = 127

        return self.system_error_print(SYSTEM_ERROR_CLI_CMD_MEM_SIZE_UNKNOWN_ARG)
    
    def mem_test(self) -> str:
        SYSTEM_ERROR_CLI_CMD_MEM_UNKNOWN_SUB_COMMAND = 103
        return self.system_error_print(SYSTEM_ERROR_CLI_CMD_MEM_UNKNOWN_SUB_COMMAND)

    def system_error_print(self, error: int) -> str:
        return f"[  ERROR]: {error}"
