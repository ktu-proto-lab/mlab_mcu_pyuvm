from cocotb.handle import SimHandleBase
from decimal import Decimal
from vif import mcu_vif
from uvc.base_if import base_if

class gpio_if(base_if):
    
    gpio_count: Decimal
    
    gpio_i: SimHandleBase
    gpio_o: SimHandleBase
    gpio_oe: SimHandleBase
    
    top_gpio_o: SimHandleBase
    top_gpio_oe: SimHandleBase

    def __init__(self, name="gpio_if", parent=None):
        super().__init__(name, parent)
        
        self.gpio_count = None
        self.gpio_i = None
        self.gpio_o = None
        self.gpio_oe = None
        self.top_gpio_o = None
        self.top_gpio_oe = None
    
    def wire(self, dut: mcu_vif):
        super().wire(dut)
        
        self.gpio_count = dut.gpio_count
        self.gpio_i = dut.gpio_i
        self.gpio_o = dut.gpio_o
        self.gpio_oe = dut.gpio_oe
        self.top_gpio_o = dut.top_gpio_o
        self.top_gpio_oe = dut.top_gpio_oe

    def drive_input(self, value: int, mask: int) -> None:
        self.top_gpio_o.value = value
        # NOTE: input mask should not conflict with the firmware of the dut.
        self.top_gpio_oe.value = mask
        
    def read_input(self, mask: int = 0xFF) -> int:
        if not self.gpio_i.value.is_resolvable:
            return None
        
        return self.gpio_i.value.integer & mask
        
    def read_output(self, mask: int = 0xFF) -> int:
        if not self.gpio_o.value.is_resolvable:
            return None
        
        return self.gpio_o.value.integer & mask
    
    def read_output_enable(self) -> int:
        if not self.gpio_oe.value.is_resolvable:
            return None
        
        return self.gpio_oe.value.integer
    
    def read_enabled_output(self, mask: int = 0xFF) -> int:
        o_value = self.read_output()
        oe_value = self.read_output_enable()
        
        if o_value is None or oe_value is None:
            return None
        
        return o_value & oe_value & mask

    def read_output_binstr(self) -> str:
        return f"0b{self.read_output():0{self.gpio_count}b}"
