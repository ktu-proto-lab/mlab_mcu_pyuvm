from pyuvm import uvm_sequencer, ConfigDB
from errors.errors import ConfigTestError
from cfg.config import Config

class GpioSequencer(uvm_sequencer):
    def __init__(self, name="GpioSequencer", parent=None):
        super().__init__(name, parent)
        self.cfg: Config = None
        
    def build_phase(self):
        super().build_phase()
        
        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigTestError("no configuration provided for gpio sequencer")
        
        self.cfg: Config = ConfigDB().get(self, "", "cfg")
        
        if not isinstance(self.cfg, Config):
            raise ConfigTestError(
                f"invalid configuration provided for gpio sequencer: expected Config, got {type(self.cfg).__name__}"
            )
