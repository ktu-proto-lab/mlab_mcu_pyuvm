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
        self.rst: SimHandleBase = dut.rst
        
        self.gpio_i: SimHandleBase = dut.gpio_i
        self.gpio_o: SimHandleBase = dut.gpio_o
        self.gpio_oe: SimHandleBase = dut.gpio_oe
        
        self.tb_gpio_o: SimHandleBase = dut.tb_gpio_o
        self.tb_gpio_oe: SimHandleBase = dut.tb_gpio_oe
        
        self.parent_name = parent.get_full_name() if hasattr(parent, "get_full_name") else "cocotb"
        self.full_name = f"{self.parent_name}.{name}"
        self.logger = SimLog(self.full_name)

    def drive_input(self, value: int, mask: int = 0x0F) -> None:
        self.tb_gpio_o.value = value
        self.tb_gpio_oe.value = mask
        
    def read_input(self) -> int:
        if not self.gpio_i.value.is_resolvable:
            return None
        
        return self.gpio_i.value.integer
        
    def read_output(self) -> int:
        if not self.gpio_o.value.is_resolvable:
            return None
        
        return self.gpio_o.value.integer
    
    def read_output_enable(self) -> int:
        if not self.gpio_oe.value.is_resolvable:
            return None
        
        return self.gpio_oe.value.integer
    
    def read_enabled_output(self) -> int:
        self.logger.debug(f"gpio_o = {self.gpio_o.value.binstr}, gpio_oe = {self.gpio_oe.value.binstr}")
        
        o_val = self.read_output()
        oe_val = self.read_output_enable()
        
        return o_val & oe_val

    def read_output_binstr(self) -> str:
        return f"0b{self.read_output():0{self.PIN_NUM}b}"
