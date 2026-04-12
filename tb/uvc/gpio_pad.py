from pyuvm import uvm_sequence_item

class GpioPad(uvm_sequence_item):
    def __init__(self, name="GpioPad"):
        super().__init__(name)
        self.state = 0x00
        self.mask = 0xFF
        self.uart_mask = 0b0000_0011

    def __str__(self):
        return hex(self.state & self.mask)
