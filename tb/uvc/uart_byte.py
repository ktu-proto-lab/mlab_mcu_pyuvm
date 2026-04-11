from pyuvm import uvm_sequence_item

class UartByte(uvm_sequence_item):
    def __init__(self, name="UartByte", byte: int = 0x00):
        super().__init__(name)
        self.val = byte

    def __str__(self):
        return hex(self.val)