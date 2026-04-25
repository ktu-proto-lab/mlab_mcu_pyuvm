from pyuvm import uvm_sequencer, ConfigDB
from tb.errors.errors import ConfigTestError

from uvc.gpio_config import GpioConfig

class GpioSequencer(uvm_sequencer):
    def __init__(self, name="GpioSequencer", parent=None):
        super().__init__(name, parent)
        self.cfg: GpioConfig = None
        
    def build_phase(self):
        super().build_phase()
        
        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigTestError("no configuration provided for gpio sequencer")
        
        self.cfg = ConfigDB().get(self, "", "cfg")
        
        if not isinstance(self.cfg, GpioConfig):
            raise ConfigTestError(
                f"invalid configuration provided for gpio sequencer: expected GpioConfig, got {type(self.cfg).__name__}"
            )
