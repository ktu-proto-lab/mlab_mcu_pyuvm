from pyuvm import uvm_agent, ConfigDB
from errors import ConfigError
from uvc.gpio_config import GpioConfig
from uvc.gpio_driver import GpioDriver
from uvc.gpio_monitor import GpioMonitor
from uvc.gpio_sequencer import GpioSequencer

class GpioAgent(uvm_agent):
    def __init__(self, name="GpioAgent", parent=None):
        super().__init__(name, parent)
        self.cfg: GpioConfig = None
        self.driver: GpioDriver = None
        self.monitor: GpioMonitor = None
        self.sequencer: GpioSequencer = None
        
    def build_phase(self):
        super().build_phase()

        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigError("no configuration provided for the gpio agent")
        
        self.cfg = ConfigDB().get(self, "", "cfg")
        
        if not self.cfg.active:
            return

        ConfigDB().set(self, "*", "cfg", self.cfg)
        
        self.driver = GpioDriver.create("driver", self)
        
        self.monitor = GpioMonitor.create("monitor", self)
        
        self.sequencer = GpioSequencer.create("sequencer", self) 

    def connect_phase(self):
        super().connect_phase()

        if not self.cfg.active:
            return
        
        self.driver.seq_item_port.connect(self.sequencer.seq_item_export)
