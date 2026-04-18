import warnings
# Disable VSC's inner warnings to not cluster the log output of the simulation
warnings.filterwarnings(action="ignore", category=DeprecationWarning, module="vsc")

import vsc
from pyuvm import uvm_sequence_item

@vsc.randobj
class GpioPad(uvm_sequence_item):
    prev_state = -1

    def __init__(self, name="GpioPad"):
        super().__init__(name)
        self.state = vsc.rand_uint8_t()
        self.mask = 0xFF
        self.uart_mask = 0b0000_0011
        self.pin_count = 8

    def __str__(self):
        return hex(int(self.state) & self.mask)

    @vsc.constraint
    def c_pad_size(self):
        self.state in vsc.rangelist(vsc.rng(0, 2**4 - 1))

    @vsc.constraint
    def c_no_sequencial_repeat_state(self):
        self.state != GpioPad.prev_state

    @vsc.constraint
    def c_no_zero_state_value(self):
        self.state != 0x00

    # vsc hook that runs automatically after self.randomize()
    def post_randomize(self):
        GpioPad.prev_state = int(self.state)

    def __eq__(self, other):
        return int(self.state) == int(other.state)
