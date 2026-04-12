from cocotb.runner import Type
from cocotb.triggers import Event
from pyuvm import uvm_subscriber, ConfigDB
from errors import ConfigError
from uvc import GpioPad
from env.mcu_config import McuConfig
from env.mcu_state_enum import McuStateEnum
from env.mcu_event_pool import McuEventPool

class McuStateObserver(uvm_subscriber):
    def __init__(self, name="McuStateObserver", parent=None):
        super().__init__(name, parent)
        self.cfg: McuConfig = None
        self.event_pool: McuEventPool = None
        self._no_pool_warned = False

    def build_phase(self):
        super().build_phase()

        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigError("no configuration provided for the state probe")

        self.cfg = ConfigDB().get(self, "", "cfg")

        if not isinstance(self.cfg, McuConfig):
            raise TypeError(f"wrong configuration provided for the state probe, expected Config, got {type(self.cfg).__name__}")

        self.event_pool = self.cfg.event_pool

    def write(self, gpio_pad: GpioPad):
        if self.event_pool is None and not self._no_pool_warned:
            self.logger.warning("state observer is active, yet no event pool provided")
            self._no_pool_warned = True
            return
        if self.event_pool is None and self._no_pool_warned:
            return

        if not isinstance(self.event_pool, McuEventPool):
            raise TypeError(f"state observer expects McuEventPool, but got {type(self.event_pool).__name__}")

        curr_state = gpio_pad.state & ~gpio_pad.uart_mask

        if curr_state & McuStateEnum.READY.value:
            self.event_pool.mcu_ready.set()
        else:
            self.event_pool.mcu_ready.clear()

        if curr_state & McuStateEnum.BUSY.value:
            self.event_pool.mcu_busy.set()
        else:
            self.event_pool.mcu_busy.clear()

        if curr_state & McuStateEnum.HALT.value:
            self.event_pool.mcu_halt.set()
        else:
            self.event_pool.mcu_halt.clear()
