from pyuvm import uvm_sequence_item

class GpioPad(uvm_sequence_item):
    def __init__(self, name="GpioPad"):
        super().__init__(name)
        self.val = 0x00
        self.mask = 0xFF
        
    def __str__(self):
        return hex(self.val & self.mask)
