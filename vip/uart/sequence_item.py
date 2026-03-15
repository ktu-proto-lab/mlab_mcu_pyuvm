from pyuvm import uvm_sequence_item

class uart_sequence_item(uvm_sequence_item):
    byte: int
    
    def __init__(self, name="uart_sequence_item", byte: int = 0x00):
        super().__init__(name)
        
        self.byte = byte
        
    def char_value(self):
        return chr(self.byte)
    
    def hex_value(self):
        return hex(self.byte)
    
    def bin_value(self):
        return bin(self.byte)
        
    def __str__(self):
        return f"{chr(self.byte)}"
