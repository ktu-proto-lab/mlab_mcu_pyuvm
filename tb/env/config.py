from pyuvm import uvm_object

from uvc import UartConfig
from vif import VirtualInterface

class Config(uvm_object):
    def __init__(self, name='Config'):
        super().__init__(name)
        self.active: bool = True
        self.uart: UartConfig = UartConfig.create("uart")
        self.trace: bool = True
        self.tracer_file_path = "sim_build/tracer.log"