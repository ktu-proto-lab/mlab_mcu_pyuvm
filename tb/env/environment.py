from pyuvm import uvm_env, ConfigDB

from errors import ConfigError
from uvc import UartAgent

from env.config import Config
from env.virtual_sequencer import VirtualSequencer

class Environment(uvm_env):
    def __init__(self, name="Environment", parent=None):
        super().__init__(name, parent)
        self.cfg: Config = None
        self.uart: UartAgent = None
        self.vseqr: VirtualSequencer = None
        
    def build_phase(self):
        super().build_phase()
        
        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigError("no configuration provided for the environment")
            
        self.cfg = ConfigDB().get(self, "", "cfg")
        
        if not isinstance(self.cfg, Config):
            raise TypeError(f"unknown configuration provided for environment: expected Config, got {type(self.cfg)}")
        
        if not self.cfg.active:
            self.logger.info("environment is not active")
            return
        
        ConfigDB().set(self, "uart", "cfg", self.cfg.uart)
        
        self.uart = UartAgent.create("uart", self)
        
        self.vseqr = VirtualSequencer.create("vseqr", self)
        
    def connect_phase(self):
        super().connect_phase()

        if not self.cfg.active:
            return
        
        if self.cfg.uart.active:
            self.vseqr = self.uart.seqr
            self.logger.debug("connected uart sequencer to virtual sequencer")
