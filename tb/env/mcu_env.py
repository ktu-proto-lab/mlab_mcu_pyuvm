from pyuvm import uvm_env, ConfigDB

from errors import ConfigError
from uvc import GpioAgent, UartAgent

from env.mcu_config import McuConfig
from env.mcu_virtual_sequencer import McuVirtualSequencer
from env.mcu_tracer import McuTracer
from env.mcu_state_observer import McuStateObserver

class McuEnv(uvm_env):
    def __init__(self, name="Environment", parent=None):
        super().__init__(name, parent)
        self.cfg: McuConfig = None
        self.uart: UartAgent = None
        self.gpio: GpioAgent = None
        self.virtual_sequencer: McuVirtualSequencer = None
        self.tracer: McuTracer = None
        self.state_observer: McuStateObserver = None

    def build_phase(self):
        super().build_phase()

        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigError("no configuration provided for the environment")

        self.cfg = ConfigDB().get(self, "", "cfg")

        if not isinstance(self.cfg, McuConfig):
            raise TypeError(f"unknown configuration provided for environment: expected Config, got {type(self.cfg)}")

        if not self.cfg.active:
            self.logger.info("environment is not active")
            return

        ConfigDB().set(self, "gpio", "cfg", self.cfg.gpio)
        self.gpio = GpioAgent.create("gpio", self)

        ConfigDB().set(self, "uart", "cfg", self.cfg.uart)
        self.uart = UartAgent.create("uart", self)

        self.virtual_sequencer = McuVirtualSequencer.create("virtual_sequencer", self)
        self.virtual_sequencer.event_pool = self.cfg.event_pool

        if self.cfg.trace:
            # TODO: just disable piping to the file, tracer will be used by other components
            ConfigDB().set(self, "tracer", "cfg", self.cfg)
            self.tracer = McuTracer.create("tracer", self)

        ConfigDB().set(self, "state_observer", "cfg", self.cfg)
        self.state_observer = McuStateObserver.create("state_observer", self)

    def connect_phase(self):
        super().connect_phase()

        if not self.cfg.active:
            return

        if self.cfg.gpio.active:
            self.virtual_sequencer.gpio = self.gpio.sequencer
            self.logger.debug("connected gpio sequencer to virtual sequencer")

            self.gpio.monitor.ap.connect(self.tracer.gpio_pad_fifo.analysis_export)
            self.logger.debug("connected gpio pad to the tracer")

            self.gpio.monitor.ap.connect(self.state_observer.analysis_export)
            self.logger.debug("connected gpio pad to the state observer")

        if self.cfg.uart.active:
            self.virtual_sequencer.uart = self.uart.sequencer
            self.logger.debug("connected uart sequencer to virtual sequencer")

            self.uart.monitor.rx_ap.connect(self.tracer.uart_rx_fifo.analysis_export)
            self.uart.monitor.tx_ap.connect(self.tracer.uart_tx_fifo.analysis_export)
            self.logger.debug("connected rx and tx ports to the tracer")
