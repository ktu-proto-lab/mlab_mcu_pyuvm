from cocotb.handle import SimHandleBase
from decimal import Decimal
from vif import McuVirtualInterface
from uvc.system_interface import SystemInterface

class GpioInterface(SystemInterface):
    def __init__(self, name="GpioInterface", parent=None):
        super().__init__(name, parent)
        self.gpio_i: SimHandleBase = None
        self.gpio_o: SimHandleBase = None
        self.gpio_oe: SimHandleBase = None
        self.top_gpio_o: SimHandleBase = None
        self.top_gpio_oe: SimHandleBase = None
        self.exit_pad_io: SimHandleBase = None
        self.gpio_count: Decimal = None

    def map(self, vif: McuVirtualInterface):
        super().map(vif)
        self.gpio_count = vif.gpio_count
        self.gpio_i = vif.gpio_i
        self.gpio_o = vif.gpio_o
        self.gpio_oe = vif.gpio_oe
        self.top_gpio_o = vif.top_gpio_o
        self.top_gpio_oe = vif.top_gpio_oe
        self.exit_pad_io = vif.exit_pad_io

    def drive_input(self, value: int, mask: int = 0xFF) -> None:
        self.top_gpio_o.value = value
        self.top_gpio_oe.value = mask

    def read_pins(self, mask: int = 0xFF) -> int:
        if not self.exit_pad_io.value.is_resolvable:
            return None
        return self.exit_pad_io.value & mask

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
