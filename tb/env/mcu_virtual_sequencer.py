from pyuvm import uvm_sequencer
from uvc.gpio import GpioSequencer
from uvc.uart import UartSequencer

class McuVirtualSequencer(uvm_sequencer):
    def __init__(self, name="McuVirtualSequencer", parent=None):
        super().__init__(name, parent)
        self.gpio_sequencer: GpioSequencer = None
        self.uart_sequencer: UartSequencer = None
