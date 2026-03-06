import warnings
# don't cluster the log output of the simulation
warnings.filterwarnings(action="ignore", category=DeprecationWarning, module="vsc")

import vsc
from pyuvm import *

@vsc.randobj
class gpio_seq_item(uvm_sequence_item):
    # Track last randomized value
    last_value = -1
    
    def __init__(self, name="gpio_seq_item", value=None):
        super().__init__(name)

        if value is None:
            self.value = vsc.rand_int8_t()
        else:
            self.value = value
    
    @vsc.constraint
    def c_lower_pins_only(self):
        self.value in vsc.rangelist(vsc.rng(1, 2**4 - 1))
        
    @vsc.constraint
    def c_no_repeat(self):
        # prevent the exact same value back-to-back
        # 0x07 0x0d 0x07 -> good
        # 0x07 0x07 0x0d -> not allowed (output Monitor won't detect the change)
        self.value != gpio_seq_item.last_value

    # VSC hook that runs automatically after self.randomize()
    def post_randomize(self):
        gpio_seq_item.last_value = self.value
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __str__(self):
        return f"{hex(int(self.value))}"
