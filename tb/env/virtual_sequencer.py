from pyuvm import uvm_sequencer
from uvc import GpioSequencer, UartSequencer

class VirtualSequencer(uvm_sequencer):
    def __init__(self, name="VirtualSequencer", parent=None):
        super().__init__(name, parent)
        self.gpio: GpioSequencer = None
        self.uart: UartSequencer = None