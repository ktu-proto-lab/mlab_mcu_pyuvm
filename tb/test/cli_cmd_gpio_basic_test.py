import pyuvm
from cocotb.triggers import FallingEdge
from test.mcu_test import McuTest

@pyuvm.test()
class CliCmdGpioBasicTest(McuTest):
    def __init__(self, name="CliCmdGpioBasicTest", parent=None):
        super().__init__(name, parent)
        
    def build_phase(self):
        super().build_phase()
        self.cfg.active_state_observer = False
        self.cfg.active_scoreboard = False
        self.cfg.uart_cfg.active = False
        self.cfg.gpio_cfg.log_debug_monitor_apply_uart_mask = True
        self.cfg.uart_cfg.log_debug_monitor_bytes_in_ascii = True
    
    
    async def run_phase(self):
        self.raise_objection()
        await super().run_phase()
        
        while True:
            await FallingEdge(self.vif.reset)
        
        self.drop_objection()
