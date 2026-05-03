from pyuvm import uvm_sequencer

from uvc.gpio_sequencer import GpioSequencer
from uvc.uart_sequencer import UartSequencer
from env.mcu_event_pool import McuEventPool
from cfg.config import Config

class McuVirtualSequencer(uvm_sequencer):
    def __init__(self, name="VirtualSequencer", parent=None):
        super().__init__(name, parent)
        self.cfg: Config = None
        self.gpio: GpioSequencer = None
        self.uart: UartSequencer = None
        self.event_pool: McuEventPool = None
