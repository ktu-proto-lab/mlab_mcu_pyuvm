from pyuvm import uvm_object
from vif import VirtualInterface

class GpioConfig(uvm_object):
    def __init__(self, name="GpioConfig"):
        super().__init__(name)
        self.active: bool = True
        self.vif: VirtualInterface = None