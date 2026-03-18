import cocotb
import pyuvm
from pyuvm import ConfigDB
from cocotb.handle import SimHandleBase
from cocotb.triggers import ClockCycles
from test import base_test
from seq import gpio_sequence
from env.gpio import gpio_env, gpio_env_config
from uvc.gpio import gpio_if

@pyuvm.test()
class gpio_simple_test(base_test):
    dut: SimHandleBase
    vif: gpio_if
    
    def build_phase(self):
        super().build_phase()
        
        self.dut = cocotb.top
        
        self.vif = gpio_if(self.dut)
        
        env_cfg = gpio_env_config.create("env_cfg")
        env_cfg.vif = self.vif
        env_cfg.input_mask = 0x0F
        env_cfg.output_mask = 0xF0
        ConfigDB().set(self, "env", "cfg", env_cfg)
        
        self.env = gpio_env.create("env", self)

    async def run_phase(self):
        self.raise_objection()
        
        await super().run_phase()
        
        # wait for main function to initialize gpio regs
        await ClockCycles(self.dut_vif.clock, 500)

        sequence = gpio_sequence.create(name="gpio_sequence")
        
        await sequence.start(self.env.input_agent.sequencer)
        
        await ClockCycles(self.dut_vif.clock, 1000)
        
        self.drop_objection()
        
    def report_phase(self):
        super().report_phase()
        
        assert self.env.scoreboard.failure == 0, (
            f"Test failed with {self.env.scoreboard.failure} scoreboard errors"
        )
