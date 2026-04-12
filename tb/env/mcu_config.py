from pyuvm import uvm_object

from uvc import GpioConfig, UartConfig
from vif import VirtualInterface
from env.mcu_event_pool import McuEventPool

class McuConfig(uvm_object):
    def __init__(self, name='Config'):
        super().__init__(name)
        self.active: bool = True
        self.vif: VirtualInterface = None
        self.uart: UartConfig = UartConfig.create("uart")
        self.gpio: GpioConfig = GpioConfig.create("gpio")
        self.trace: bool = True
        self.tracer_file_path = "sim_build/tracer.log"
        self.event_pool = McuEventPool.create("event_pool")
