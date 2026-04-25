from pyuvm import uvm_sequencer, ConfigDB
from errors import ConfigTestError

from uvc.uart_config import UartConfig

class UartSequencer(uvm_sequencer):
    def __init__(self, name="UartSequencer", parent=None):
        super().__init__(name, parent)
        self.cfg: UartConfig = None
        
    def build_phase(self):
        super().build_phase()
        
        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigTestError("no provided configuration for uart sequencer")
        
        self.cfg = ConfigDB().get(self, "", "cfg")
        
        if not isinstance(self.cfg, UartConfig):
            raise ConfigTestError(
                f"invalid configuration type for uart sequencer, expected UartConfig, got {type(self.cfg).__name__}"
            )
        