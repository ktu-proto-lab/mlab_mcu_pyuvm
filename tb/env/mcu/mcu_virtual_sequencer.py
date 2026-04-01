from pyuvm import uvm_sequencer
from uvc.gpio import gpio_sequencer
from uvc.uart import uart_sequencer

class mcu_virtual_sequencer(uvm_sequencer):
    def build_phase(self):
        super().build_phase()
        self.gpio_sequencer: gpio_sequencer = None
        self.uart_sequencer: uart_sequencer = None
 