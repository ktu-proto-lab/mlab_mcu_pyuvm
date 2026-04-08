from pyuvm import uvm_sequencer
from uvc.uart.uart_interface import UartInterface

class UartSequencer(uvm_sequencer):
    def __init__(self, name="UartSequencer", parent=None):
        super().__init__(name, parent)
        self.vif: UartInterface = None
