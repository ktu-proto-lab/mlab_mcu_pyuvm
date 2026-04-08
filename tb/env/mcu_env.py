from pyuvm import uvm_env, uvm_object, ConfigDB
from uvc.gpio import GpioAgent
from uvc.uart import UartAgent
from error import ConfigError
from env.uart_tracer import UartTracer


class McuEnv(uvm_env):
    class Config(uvm_object):
        def __init__(self, name="McuEnvConfig"):
            super().__init__(name)
            self.is_active: bool = True
            self.gpio: GpioAgent.Config = GpioAgent.Config.create("gpio")
            self.uart: UartAgent.Config = UartAgent.Config.create("uart")
            self.uart_tracer: UartTracer.Config = UartTracer.Config.create("uart_tracer")

    def __init__(self, name="uvm_env", parent=None):
        super().__init__(name, parent)
        self.cfg: McuEnv.Config = None
        self.gpio: GpioAgent = None
        self.uart: UartAgent = None
        self.uart_tracer: UartTracer = None

    def build_phase(self):
        super().build_phase()
        self.cfg = ConfigDB().get(self, "", "cfg")
        if self.cfg is None:
            raise ConfigError("no configuration provided for the environment", self)
        if not self.cfg.is_active:
            self.logger.info("mcu environment is not active")
            return
        if self.cfg.gpio is None:
            raise ConfigError("no gpio configuration provided for the environment", self)
        ConfigDB().set(self, "gpio", "cfg", self.cfg.gpio)
        self.gpio = GpioAgent.create("gpio", self)
        if self.cfg.uart is None:
            raise ConfigError("no uart configuration provided for the environment", self)
        ConfigDB().set(self, "uart", "cfg", self.cfg.uart)
        self.uart = UartAgent.create("uart", self)
        if self.cfg.uart_tracer is None:
            raise ConfigError("no uart tracer configuration provided for the environment", self)
        ConfigDB().set(self, "uart_tracer", "cfg", self.cfg.uart_tracer)
        self.uart_tracer = UartTracer.create("uart_tracer", self)

    def connect_phase(self):
        super().connect_phase()
        if not self.cfg.is_active:
            return
        if not self.cfg.uart_tracer.is_active:
            return
        if self.cfg.uart_tracer.enable_transmit_stream:
            self.uart.driver.analysis_port.connect(self.uart_tracer.transmit_export)
        if self.cfg.uart_tracer.enable_receive_stream:
            self.uart.monitor.analysis_port.connect(self.uart_tracer.receive_export)