from cocotb.runner import Type
from cocotb.triggers import Event
from pyuvm import uvm_subscriber, ConfigDB
from errors import ConfigTestError
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
        self.prev_state = None

    def build_phase(self):
        super().build_phase()

        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigTestError("no configuration provided for the state probe")

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

        curr_state &= (McuStateEnum.READY.value | McuStateEnum.BUSY.value | McuStateEnum.DEBUG.value)

        if curr_state == 0:
            return

        if curr_state == self.prev_state:
            return

        self.logger.debug(f"mcu state gpio pad pin values 0b{(curr_state >> 5) & 0b111:03b}")

        if curr_state & McuStateEnum.READY.value and not self.event_pool.mcu_ready.is_set():
            self.logger.debug("mcu state ready event set")
            self.event_pool.mcu_ready.set()

        if curr_state & McuStateEnum.BUSY.value and not self.event_pool.mcu_busy.is_set():
            self.logger.debug("mcu state busy event set")
            self.event_pool.mcu_busy.set()

        if curr_state & McuStateEnum.DEBUG.value and not self.event_pool.mcu_debug.is_set():
            self.logger.debug("mcu state halt event set")
            self.event_pool.mcu_debug.set()

        self.prev_state = curr_state
