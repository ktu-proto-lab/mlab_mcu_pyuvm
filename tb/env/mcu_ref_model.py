from pyuvm import uvm_object
from env.mcu_config import McuConfig
from env.mcu_memory_mirror import McuMemoryMirror
from errors import ConfigError, NotImplementedError

class McuRefModel(uvm_object):
    def __init__(self, name='McuRefModel'):
        super().__init__(name)
        self.cfg: McuConfig = None
        self.memory: McuMemoryMirror = McuMemoryMirror.create("memory")

    def config_assign_check(self):
        if self.cfg is None:
            raise ConfigError("no configuration provided for mcu reference model")

        if not isinstance(self.cfg, McuConfig):
            raise ConfigError(f"expected assigned configuration to be McuConfig, actual is {type(self.cfg).__name__}")

    def init_memory(self):
        raise NotImplementedError()
