from pyuvm import uvm_object

from vif.mcu_virtual_interface import McuVirtualInterface

class GpioConfig(uvm_object):
    def __init__(self, name="GpioConfig"):
        super().__init__(name)
        self.active: bool = True
        self.vif: McuVirtualInterface = None
        self.log_debug_monitor_apply_uart_mask: bool = False
        self.uart_mask: int = 0b00000011
        self.pin_count: int = 10
