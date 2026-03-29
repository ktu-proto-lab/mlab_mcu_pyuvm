from pyuvm import uvm_object
from uvc.gpio import gpio_if, gpio_config

class gpio_env_config(uvm_object):
    vif: gpio_if
    input_mask: int = 0xFF
    output_mask: int = 0xFF
    
    def __init__(self, name="gpio_env_config"):
        super().__init__(name)