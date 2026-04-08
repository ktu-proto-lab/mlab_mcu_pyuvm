from pyuvm import uvm_agent, uvm_analysis_port, uvm_object, ConfigDB
from uvc.uart.uart_interface import UartInterface
from uvc.uart.uart_driver import UartDriver
from uvc.uart.uart_monitor import UartMonitor
from uvc.uart.uart_sequencer import UartSequencer
from error import ConfigError

class UartAgent(uvm_agent):
    class Config(uvm_object):
        def __init__(self, name="UartAgentConfig"):
            super().__init__(name)
            self.is_active: bool = True
            self.vif: UartInterface = None
            self.driver: UartDriver.Config = UartDriver.Config.create("driver")
            self.monitor: UartMonitor.Config = UartMonitor.Config.create("monitor")

    def __init__(self, name="UartAgent", parent=None):
        super().__init__(name, parent)
        self.cfg: UartAgent.Config = None
        self.driver: UartDriver = None
        self.monitor: UartMonitor = None
        self.sequencer: UartSequencer = None
        self.receive_analysis_port: uvm_analysis_port = None
        self.transmit_analysis_port: uvm_analysis_port = None

    def build_phase(self):
        super().build_phase()
        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigError("no configuration provided for the uart agent", self)
        self.cfg = ConfigDB().get(self, "", "cfg")
        if not self.cfg.is_active:
            self.logger.info("uart agent is not active")
            return
        if self.cfg.vif is None:
            raise ConfigError("no provided interface for the uart agent", self)
        if self.cfg.driver is None:
            raise ConfigError("no provided configuration for uart driver", self)
        self.cfg.driver.vif = self.cfg.vif
        ConfigDB().set(self, "driver", "cfg", self.cfg.driver)
        self.driver = UartDriver.create("driver", self)
        self.transmit_analysis_port = uvm_analysis_port.create("transmit_analysis_port", self)
        if self.cfg.monitor is None:
            raise ConfigError("no provided configuration for uart monitor", self)
        self.cfg.monitor.vif = self.cfg.vif
        ConfigDB().set(self, "monitor", "cfg", self.cfg.monitor)
        self.monitor = UartMonitor.create("monitor", self)
        self.receive_analysis_port = uvm_analysis_port.create("receive_analysis_port", self)
        self.sequencer = UartSequencer.create("sequencer", self)
        self.sequencer.vif = self.cfg.vif

    def connect_phase(self):
        super().connect_phase()
        if not self.cfg.is_active:
            return
        self.driver.seq_item_port.connect(self.sequencer.seq_item_export)
        self.driver.analysis_port.connect(self.transmit_analysis_port)
        self.monitor.analysis_port.connect(self.receive_analysis_port)
