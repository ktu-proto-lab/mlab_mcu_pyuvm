from pyuvm import uvm_object

from uvc import GpioConfig, UartConfig
from vif import McuVirtualInterface
from env.mcu_event_pool import McuEventPool

class McuConfig(uvm_object):
    def __init__(self, name='Config'):
        super().__init__(name)
        self.env_enable: bool = True
        self.vif: McuVirtualInterface = None
        self.uart_cfg: UartConfig = UartConfig.create("uart_cfg")
        self.gpio_cfg: GpioConfig = GpioConfig.create("gpio_cfg")
        self.tracer_log_enable: bool = True
        self.tracer_log_filepath: str = "sim_build/tracer.log"
        self.event_pool = McuEventPool.create("event_pool")
        self.scoreboard_enable: bool = True
        # TODO: change to dynamic by test name
        self.mem_path: str = f"/home/mcu/uvm/sw/test/command_test/build/"
