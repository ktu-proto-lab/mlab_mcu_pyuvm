from cocotb.triggers import Event
from pyuvm import uvm_object

class McuEventPool(uvm_object):
    def __init__(self, name="McuEventPool"):
        super().__init__(name)
        self.mcu_ready  = Event("ready")
        self.mcu_busy   = Event("busy")
        self.mcu_debug  = Event("halt")
