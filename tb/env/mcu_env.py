from pyuvm import uvm_env, uvm_object, ConfigDB
from uvc.gpio import GpioAgent, GpioInterface
from vif import McuVirtualInterface
from log.error import ConfigError

class McuEnv(uvm_env):
    class Config(uvm_object):
        def __init__(self, name="McuEnvConfig"):
            super().__init__(name)
            self.gpio_if: GpioInterface = None
            self.gpio: GpioAgent.Config = GpioAgent.Config.create("gpio")
            
    
    def __init__(self, name="uvm_env", parent=None):
        super().__init__(name, parent)
        self.cfg: McuEnv.Config = None
        self.gpio_agent: GpioAgent = None
    
    def build_phase(self):
        super().build_phase()
        self.cfg = ConfigDB().get(self, "", "cfg")
        if self.cfg is None:
            raise ConfigError("no configuration provided for the environment", self)
        if self.cfg.gpio_if is None:
            raise ConfigError("no gpio interface provided in configuration", self)
        self.cfg.gpio.vif = self.cfg.gpio_if
        ConfigDB().set(self, "gpio_agent", "cfg", self.cfg.gpio)
        self.gpio_agent = GpioAgent.create("gpio_agent", self)
        
    def connect_phase(self):
        super().connect_phase()
