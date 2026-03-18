from pyuvm import uvm_object
from uvc.gpio.gpio_if import gpio_if

class gpio_monitor_config(uvm_object):
    mask: int = 0xFF
    
    def __init__(self, name="gpio_driver_config"):
        super().__init__(name)