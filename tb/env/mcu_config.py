from pyuvm import uvm_object

from uvc import GpioConfig, UartConfig
from vif import VirtualInterface

class McuConfig(uvm_object):
    def __init__(self, name='Config'):
        super().__init__(name)
        self.active: bool = True
        self.vif: VirtualInterface = None
        self.uart: UartConfig = UartConfig.create("uart")
        self.gpio: GpioConfig = GpioConfig.create("gpio")
        self.trace: bool = True
        self.tracer_file_path = "sim_build/tracer.log"
