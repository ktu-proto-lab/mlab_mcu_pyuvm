import vsc
from pyuvm import *

@vsc.randobj
class gpio_seq_item(uvm_sequence_item):
    def __init__(self, name="gpio_seq_item", value=0):
        super().__init__(name)

        self.value = vsc.rand_int8_t()
    
    @vsc.constraint
    def c_lower_pins_only(self):
        self.value in vsc.rangelist(vsc.rng(0, 2**4 - 1))

    def __eq__(self, other):
        return self.value == other.value
    
    def __str__(self):
        return f"{hex(int(self.value))}"
