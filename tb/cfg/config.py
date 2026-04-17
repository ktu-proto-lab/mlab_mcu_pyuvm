from pyuvm import uvm_object

from vif.mcu_virtual_interface import McuVirtualInterface
from uvc.gpio_config import GpioConfig
from uvc.uart_config import UartConfig
from env.mcu_memory_config import McuMemoryConfig
from env.mcu_event_pool import McuEventPool
from env.mcu_simulator import McuSimulatorEnum

class Config(uvm_object):
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
        self.mem_path: str = None
        self.mem_cfg: McuMemoryConfig = McuMemoryConfig.create("mem_cfg")
        self.simulator: McuSimulatorEnum = None
