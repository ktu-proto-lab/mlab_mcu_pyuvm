import cocotb
import logging
import os
from cocotb.handle import SimHandleBase
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
        
        # Let set log level from the sim/Makefile itself, default to info
        level_str = os.getenv("COCOTB_LOG_LEVEL", "INFO").upper()
    
        # Convert string (e.g., "DEBUG") to logging constant (e.g., logging.DEBUG)
        log_level = getattr(logging, level_str, logging.INFO)
        
        # Apply to all pyuvm components
        uvm_report_object.set_default_logging_level(log_level)
        
        self.dut: SimHandleBase = cocotb.top
        
        self.env = gpio_env(name="env", parent=self)

    async def run_phase(self):
        await super().run_phase()
        
        self.raise_objection()
        
        cocotb.start_soon(Clock(self.dut.clk, 10, units='ns').start())
        
        self.dut.rst.value = 0
        await ClockCycles(self.dut.clk, 10)
        self.dut.rst.value = 1
        
        # wait for main function to initialize gpio regs
        await ClockCycles(self.dut.clk, 500)

        seq = gpio_4bit_rnd_seq(name="gpio_4bit_rnd_seq")
        
        await seq.start(self.env.agent.sequencer)
        
        await ClockCycles(self.dut.clk, 1000)
        
        self.drop_objection()
        
    def report_phase(self):
        super().report_phase()
        
        assert self.env.scoreboard.failure == 0, (
            f"Test failed with {self.env.scoreboard.failure} scoreboard errors"
        )
