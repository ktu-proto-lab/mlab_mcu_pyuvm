from pyuvm import uvm_object

class gpio_driver_config(uvm_object):
    mask: int = 0xFF
    
    def __init__(self, name="gpio_driver_config"):
        super().__init__(name)
    