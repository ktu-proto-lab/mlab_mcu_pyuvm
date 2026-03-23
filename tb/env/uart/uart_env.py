from pyuvm import uvm_env, ConfigDB
from typing import cast
from uvc.uart import uart_if, uart_agent
from env.uart.uart_env_config import uart_env_config

class uart_env(uvm_env):
    def build_phase(self):
        super().build_phase()

        if not ConfigDB().exists(self, "", "cfg"):
            self.logger.error("environment can not be built - no configuration provided")
            
        self.cfg = cast(uart_env_config, ConfigDB().get(self, "", "cfg"))
        
        if not self.cfg.is_set:
            self.logger.error("provided configuration is not set")
        
        self.vif: uart_if = self.cfg.vif
        
        self.agent: uart_agent = uart_agent.create("agent", self)

        ConfigDB().set(self, "*", "vif", self.vif)
