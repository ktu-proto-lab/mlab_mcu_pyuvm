from pyuvm import uvm_sequence_item

class uart_sequence_item(uvm_sequence_item):
    def __init__(self, name="uart_sequence_item", byte: int = 0x00):
        super().__init__(name)
        
        self.byte: int = byte
        
    def __str__(self):
        return f"{chr(self.byte)}"