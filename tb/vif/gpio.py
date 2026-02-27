from typing import List
from cocotb.handle import SimHandleBase

class gpio:
    """
    @brief GPIO Module's Virtual Interface

    - Total external pads are 10 
    - Pads 0-7 are usable GPIO pins
    - Logical GPIO_PIN_0 corresponds to LSB
    """

    PIN_NUM: int = 8

    def __init__(self, dut: SimHandleBase):
        self.clk = dut.clk
        
        self.pins: List[SimHandleBase] = []

        for i in range(self.PIN_NUM):
            self.pins.append(dut.ext_pad_io[i])

    def _check_pin(self, pin: int) -> None:
        if not 0 <= pin < self.PIN_NUM:
            raise IndexError(f"GPIO pin {pin} out of range (0:{self.PIN_NUM - 1})")

    def set_pin(self, pin: int) -> None:
        self._check_pin(pin)
        self.pins[pin].value = 1
        
    def set_pins(self, value: int):
        if not 0 <= value < 2**self.PIN_NUM:
            raise ValueError(f"Given value {value} exceeds physical GPIO pins: {self.PIN_NUM}")
        for idx in range(self.PIN_NUM):
            self.pins[idx].value = (value >> idx) & 1; 
    
    def reset_pin(self, pin: int) -> None:
        self._check_pin(pin)
        self.pins[pin].value = 0

    def read_pin(self, pin: int) -> int:
        self._check_pin(pin)
        return self.pins[pin].value.integer
    
    def read_pins(self) -> int:
        value = 0
        for i, pin in enumerate(self.pins):
            value |= (pin.value.integer << i)
        return value
    
    def read_pins_binsrt(self) -> str:
        value = self.read_pins()
        return f"0b{value:08b}"
