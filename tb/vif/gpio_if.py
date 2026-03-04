from cocotb.log import SimLog
from cocotb.handle import SimHandleBase

class gpio_if:
    """
    @brief GPIO Module's Virtual Interface

    - Total external pads are 10 
    - Pads 0-7 are usable GPIO pins
    - Logical GPIO_PIN_0 corresponds to LSB
    """

    PIN_NUM: int = 8

    def __init__(self, dut: SimHandleBase, name="gpio_if", parent=None):
        self.clk: SimHandleBase = dut.clk
        
        self.gpio_i: SimHandleBase = dut.gpio_i
        self.gpio_o: SimHandleBase = dut.gpio_o
        self.gpio_oe: SimHandleBase = dut.gpio_oe
        
        self.parent_name = parent.get_full_name() if hasattr(parent, "get_full_name") else "cocotb"
        self.full_name = f"{self.parent_name}.{name}"
        self.logger = SimLog(self.full_name)

    def drive_pins(self, value) -> None:
        self.gpio_i.value = value
        
    def read_pins(self) -> int:
        if not self.gpio_o.value.is_resolvable:
            self.logger.warning(
                    f"GPIO pin signals contain unresolvable values: {self.gpio_o.value.binstr}, returning 0")
            return 0
        else:
            return self.gpio_o.value.integer


    def read_pins_binstr(self) -> str:
        return f"0b{self.read_pins():0{self.PIN_NUM}b}"
