from pyuvm import uvm_object

from vif.mcu_virtual_interface import McuVirtualInterface

class UartConfig(uvm_object):
    def __init__(self, name="UartConfig"):
        super().__init__(name)
        self.active: bool = True
        # TODO: monitoring-only option
        # self.is_passive: bool = False
        self.vif: McuVirtualInterface = None
        self.log_monitor_bytes_in_ascii: bool = False
