from pyuvm import uvm_object
from uvc.uart import uart_if

class uart_env_config(uvm_object):
    def __init__(self, name="uart_env_config"):
        super().__init__(name)
        
        self.vif: uart_if = None
        self.is_set: bool = False
