from cocotb.runner import Type
from pyuvm import uvm_agent, uvm_object, ConfigDB, uvm_analysis_port

from errors import ConfigTestError

from cfg.config import Config
from uvc.uart_driver import UartDriver
from uvc.uart_monitor import UartMonitor
from uvc.uart_sequencer import UartSequencer
from uvc.uart_config import UartConfig

class UartAgent(uvm_agent):
    def __init__(self, name="UartAgent", parent=None):
        super().__init__(name, parent)
        self.cfg: UartConfig = None
        self.driver: UartDriver = None
        self.monitor: UartMonitor = None
        self.sequencer: UartSequencer = None

    def build_phase(self):
        super().build_phase()

        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigTestError("cfguration not given to uart agent")

        self.cfg = ConfigDB().get(self, "", "cfg")

        if not isinstance(self.cfg, Config):
            raise TypeError(
                f"expected provided configuration to be Config, got {type(self.cfg).__name__}"
            )

        if not isinstance(self.cfg.uart_cfg, UartConfig):
            raise TypeError("unknown type provided for uart agent configuration")

        if not self.cfg.uart_cfg.active:
            self.logger.info("uart is not active")
            return

        # BUG: I think missmatching names gives a bug, don't know it yet
        self.driver = UartDriver.create("driver", self)

        self.monitor = UartMonitor.create("monitor", self)

        self.sequencer = UartSequencer.create("sequencer", self)

    def connect_phase(self):
        super().connect_phase()

        if not self.cfg.uart_cfg.active:
            return

        self.driver.seq_item_port.connect(self.sequencer.seq_item_export)
