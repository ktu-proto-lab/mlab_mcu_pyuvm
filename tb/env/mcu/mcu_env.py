from pyuvm import uvm_env, uvm_object, ConfigDB
from env.mcu.mcu_virtual_sequencer import mcu_virtual_sequencer
from error import env_config_error
from uvc.gpio import gpio_agent, gpio_config
from uvc.uart import uart_agent, uart_config
from vif import mcu_vif

class mcu_env_config(uvm_object):
    def __init__(self, name="mcu_env_config"):
        super().__init__(name)
        self.vif: mcu_vif = None
        self.gpio_enable: bool = None
        self.uart_enable: bool = None
        self.i2c_enable: bool = None # TODO: implement i2c agent
        self.gpio_cfg: gpio_config = None
        self.uart_cfg: uart_config = None

class mcu_env(uvm_env):
    def __init__(self, name="uvm_env", parent=None):
        super().__init__(name, parent)
        self.cfg: mcu_env_config = None
        self.vif: mcu_vif = None
        self.gpio_agent: gpio_agent = None
        self.uart_agent: uart_agent = None
        self.virtual_sequencer: mcu_virtual_sequencer = None
        self.ref_model = None # TODO: implement golden reference model
        self.scoreboard = None # TODO: implement scoreboard
        self.coverage = None # TODO: implement coverage
    
    def build_phase(self):
        super().build_phase()
        if not ConfigDB().exists(self, "", "cfg"):
            raise env_config_error("configuration does not exist", self)
        self.cfg = ConfigDB().get(self, "", "cfg")
        self.vif = self.cfg.vif
        if self.cfg.gpio_enable:
            ConfigDB().set(self, "gpio_agent", "cfg", self.cfg.gpio_cfg)
            self.gpio_agent = gpio_agent.create("gpio_agent", self)
        if self.cfg.uart_enable:
            ConfigDB().set(self, "uart_agent", "cfg", self.cfg.uart_cfg)
            self.uart_agent = uart_agent.create("uart_agent", self)
        self.virtual_sequencer = mcu_virtual_sequencer.create("virtual_sequencer", self)
        
    def connect_phase(self):
        super().connect_phase()
        if self.cfg.gpio_enable:
            self.virtual_sequencer.gpio_sequencer = self.gpio_agent.sequencer
        if self.cfg.uart_enable:
            self.virtual_sequencer.uart_sequencer = self.uart_agent.sequencer
