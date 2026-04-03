import warnings
# Disable VSC's inner warnings to not cluster the log output of the simulation
warnings.filterwarnings(action="ignore", category=DeprecationWarning, module="vsc")

import vsc
from pyuvm import uvm_sequence_item

@vsc.randobj
class GpioTransaction(uvm_sequence_item):
    _last_value = -1

    def __init__(self, name="gpio_sequence_item", value=None):
        super().__init__(name)
        # Track last randomized value
        if value is None:
            self.value = vsc.rand_int8_t()
        else:
            self.value = value

    @vsc.constraint
    def c_lower_pins_only(self):
        self.value in vsc.rangelist(vsc.rng(0, 2**4 - 1))

    @vsc.constraint
    def c_no_repeat(self):
        # prevent the exact same value back-to-back
        # 0x07 0x0d 0x07 -> good
        # 0x07 0x07 0x0d -> not allowed (output Monitor won't detect the change)
        self.value != GpioTransaction._last_value

    # VSC hook that runs automatically after self.randomize()
    def post_randomize(self):
        GpioTransaction._last_value = self.value

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return f"{hex(int(self.value))}"
