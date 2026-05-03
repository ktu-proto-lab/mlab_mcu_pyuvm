from pyuvm import uvm_subscriber
from uvc.gpio_pad import GpioPad
from cfg.config import Config

class McuGpioPadState(uvm_subscriber):
    def __init__(self, name="McuGpioPadState", parent=None):
        super().__init__(name, parent)
        self.state: int = None
        self.cfg: Config = None
    
    def write(self, item: GpioPad):
        self.state = item.state