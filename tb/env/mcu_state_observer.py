from cocotb.triggers import Event
from pyuvm import uvm_subscriber, ConfigDB
from errors import ConfigError
from uvc import GpioPad
from env.mcu_config import McuConfig
from env.mcu_state_enum import McuStateEnum

class McuStateObserver(uvm_subscriber):
    def __init__(self, name="McuStateObserver", parent=None):
        super().__init__(name, parent)
        self.cfg: McuConfig = None
        self.ready: Event = None
        self.busy: Event = None
        self.halt: Event = None

    def build_phase(self):
        super().build_phase()

        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigError("no configuration provided for the state probe")

        self.cfg = ConfigDB().get(self, "", "cfg")

        if not isinstance(self.cfg, McuConfig):
            raise TypeError(f"wrong configuration provided for the state probe, expected Config, got {type(self.cfg).__name__}")

        self.ready = Event("ready")
        self.busy = Event("busy")
        self.halt = Event("halt")

    def write(self, gpio_pad: GpioPad):
        curr_state = gpio_pad.state & ~gpio_pad.uart_mask

        if curr_state & McuStateEnum.READY.value:
            self.ready.set()
        else:
            self.ready.clear()

        if curr_state & McuStateEnum.BUSY.value:
            self.busy.set()
        else:
            self.busy.clear()

        if curr_state & McuStateEnum.HALT.value:
            self.halt.set()
        else:
            self.halt.clear()
