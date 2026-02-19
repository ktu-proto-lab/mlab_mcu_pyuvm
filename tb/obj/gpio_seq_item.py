from pyuvm import *

class gpio_seq_item(uvm_sequence_item):
    def __init__(self, name="gpio_seq_item", value=0):
        super().__init__(name)

        self.value = value

    def __eq__(self, other):
        return self.pin == other.pin and self.value == other.value
    
