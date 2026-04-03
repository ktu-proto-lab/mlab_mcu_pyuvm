from pyuvm import uvm_env, uvm_object, ConfigDB
from uvc.gpio import GpioAgent
from uvc.uart import UartAgent
from log.error import ConfigError

class McuEnv(uvm_env):
    class Config(uvm_object):
        def __init__(self, name="McuEnvConfig"):
            super().__init__(name)
            # TODO (refac): maybe move mapping to the environment
            self.gpio: GpioAgent.Config = GpioAgent.Config.create("gpio")
            self.uart: UartAgent.Config = UartAgent.Config.create("uart")
            
    
    def __init__(self, name="uvm_env", parent=None):
        super().__init__(name, parent)
        self.cfg: McuEnv.Config = None
        self.gpio: GpioAgent = None
        self.uart: UartAgent = None
    
    def build_phase(self):
        super().build_phase()
        self.cfg = ConfigDB().get(self, "", "cfg")
        if self.cfg is None:
            raise ConfigError("no configuration provided for the environment", self)
        if self.cfg.gpio is None:
            raise ConfigError("no gpio configuration provided for the environment", self)
        ConfigDB().set(self, "gpio", "cfg", self.cfg.gpio)
        self.gpio = GpioAgent.create("gpio", self)
        if self.cfg.uart is None:
            raise ConfigError("no uart configuration provided for the environment", self)
        ConfigDB().set(self, "uart", "cfg", self.cfg.uart)
        self.uart = UartAgent.create("uart", self)
        
    def connect_phase(self):
        super().connect_phase()
