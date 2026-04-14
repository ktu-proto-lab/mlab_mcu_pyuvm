from pyuvm import uvm_object

from vif import McuVirtualInterface

class UartConfig(uvm_object):
    def __init__(self, name="UartConfig"):
        super().__init__(name)
        self.active: bool = True
        # TODO: monitoring-only option
        # self.is_passive: bool = False
        self.vif: McuVirtualInterface = None
