from pyuvm import uvm_sequence_item

class UartTransaction(uvm_sequence_item):
    def __init__(self, name="uart_transaction", byte: int = 0xFF):
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
