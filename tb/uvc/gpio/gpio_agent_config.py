from enum import Enum
from pyuvm import uvm_object
from uvc.gpio.gpio_if import gpio_if
from uvc.gpio.gpio_driver_config import gpio_driver_config
from uvc.gpio.gpio_monitor_config import gpio_monitor_config

class gpio_agent_config(uvm_object):
    class port_type_enum(Enum):
        INPUT = 1
        OUTPUT = 2
    
    vif: gpio_if
    is_active: bool
    port_type: port_type_enum
    driver_cfg: gpio_driver_config
    monitor_cfg: gpio_monitor_config
    
    def __init__(self, name="gpio_agent_config"):
        super().__init__(name)
        
        self.vif = None
        self.is_active = None
        self.port_type = None
        self.driver_cfg = None
        self.monitor_cfg = None
        