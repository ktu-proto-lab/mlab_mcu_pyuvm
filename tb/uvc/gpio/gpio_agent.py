from pyuvm import uvm_agent, uvm_analysis_port, ConfigDB, uvm_object
from log.error import ConfigError
from uvc.gpio.gpio_driver import GpioDriver
from uvc.gpio.gpio_monitor import GpioMonitor
from uvc.gpio.gpio_sequencer import GpioSequencer
from uvc.gpio.gpio_interface import GpioInterface

class GpioAgent(uvm_agent):
    class Config(uvm_object):
        def __init__(self, name="GpioAgentConfig"):
            super().__init__(name)
            self.is_active: bool = True
            self.vif: GpioInterface = None
            self.driver: GpioDriver.Config = GpioDriver.Config.create("driver")
            self.monitor: GpioMonitor.Config = GpioMonitor.Config.create("monitor")
            
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.cfg: GpioAgent.Config = None
        self.driver: GpioDriver = None
        self.monitor: GpioMonitor = None
        self.sequencer: GpioSequencer = None
        self.analysis_port: uvm_analysis_port = None

    def build_phase(self):
        super().build_phase()
        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigError("no configuration provided for the gpio agent", self)
        self.cfg = ConfigDB().get(self, "", "cfg")
        if not self.cfg.is_active:
            self.logger.info("gpio agent is not active")
            return
        if self.cfg.vif is None:
            raise ConfigError("no provided interface for the gpio agent", self)
        self.cfg.driver.vif = self.cfg.vif
        ConfigDB().set(self, "driver", "cfg", self.cfg.driver)
        self.driver = GpioDriver.create("driver", self)
        self.cfg.monitor.vif = self.cfg.vif
        ConfigDB().set(self, "monitor", "cfg", self.cfg.monitor)
        self.monitor = GpioMonitor.create("monitor", self)
        self.sequencer = GpioSequencer.create("sequencer", self)
        self.analysis_port = uvm_analysis_port("analysis_port", self)
        

    def connect_phase(self):
        super().connect_phase()
        if not self.cfg.is_active:
            return
        self.driver.seq_item_port.connect(self.sequencer.seq_item_export)
        self.monitor.analysis_port.connect(self.analysis_port)
