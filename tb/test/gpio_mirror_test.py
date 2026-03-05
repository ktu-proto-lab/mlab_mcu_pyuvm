import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
import pyuvm
from pyuvm import *
from tb.env.gpio_env import gpio_env
from vip.gpio.gpio_sequence import gpio_4bit_rnd_seq

@pyuvm.test()
class gpio_mirror_test(uvm_test):
    def build_phase(self):
        super().build_phase()
        
        self.env = gpio_env(name="env", parent=self)

    async def run_phase(self):
        await super().run_phase()
        
        self.raise_objection()
        
        cocotb.start_soon(Clock(self.env.dut.clk, 10, units='ns').start())
        
        self.env.dut.rst.value = 0
        await ClockCycles(self.env.dut.clk, 10)
        self.env.dut.rst.value = 1
        
        # wait for main function to initialize gpio regs
        await ClockCycles(self.env.dut.clk, 500)

        seq = gpio_4bit_rnd_seq(name="gpio_4bit_rnd_seq")
        
        await seq.start(self.env.agent.sequencer)
        
        self.drop_objection()
        
    def report_phase(self):
        super().report_phase()
        
        assert self.env.scoreboard.failure == 0, (
            f"Test failed with {self.env.scoreboard.failure} scoreboard errors"
        )
