from pyuvm import uvm_sequencer
from uvc import UartSequencer

class VirtualSequencer(uvm_sequencer):
    def __init__(self, name="VirtualSequencer", parent=None):
        super().__init__(name, parent)
        self.uart: UartSequencer = None