from pyuvm import uvm_sequencer

from uvc.gpio_sequencer import GpioSequencer
from uvc.uart_sequencer import UartSequencer
from env.mcu_event_pool import McuEventPool

class McuVirtualSequencer(uvm_sequencer):
    def __init__(self, name="VirtualSequencer", parent=None):
        super().__init__(name, parent)
        self.gpio: GpioSequencer = None
        self.uart: UartSequencer = None
        self.event_pool: McuEventPool = None
