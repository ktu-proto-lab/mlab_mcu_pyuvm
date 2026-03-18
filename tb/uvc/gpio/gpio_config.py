from enum import Enum
from pyuvm import uvm_object, uvm_active_passive_enum
from uvc.gpio.gpio_if import gpio_if

class gpio_config(uvm_object):
    class port_type_enum(Enum):
        INPUT = 1
        OUTPUT = 2
    
    vif: gpio_if
    is_active: bool
    port_type: port_type_enum
    
    def __init__(self, name="gpio_agent_config"):
        super().__init__(name)
        
        self.vif = None
        self.is_active = None
        self.port_type = None
        