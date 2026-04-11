from cocotb.triggers import Event
from pyuvm import uvm_component, ConfigDB
from config import Config
from errors import ConfigError

class StateProbe(uvm_component):
    def __init__(self, name="StateProbe", parent=None):
        super().__init__(name, parent)
        self.cfg: Config = None
        self.ready: Event = None
        self.busy: Event = None
        self.halt: Event = None
        
    def build_phase(self):
        super().build_phase()

        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigError("no configuration provided for the state probe")
        
        self.cfg = ConfigDB().get(self, "", "cfg")
        
        if not isinstance(self.cfg, Config):
            raise TypeError(f"wrong configuration provided for the state probe, expected Config, got {type(self.cfg).__name__}")

        self.ready = Event("ready")
        self.busy = Event("busy")
        self.halt = Event("halt")
        
        