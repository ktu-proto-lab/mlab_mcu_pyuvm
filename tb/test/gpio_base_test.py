import cocotb
import logging
import os
from cocotb.clock import Clock
from cocotb.handle import SimHandleBase
from cocotb.triggers import ClockCycles
from pyuvm import uvm_test, uvm_report_object
from tb.env.gpio_env import gpio_env

# TODO (06.03.26): check if the running program on the DUT exists.
class gpio_base_test(uvm_test):
    def __init__(self, name="gpio_base_test", parent=None):
        # Let set log level from the Makefile itself, default to info
        level: str = os.getenv(key="COCOTB_LOG_LEVEL", default="INFO").upper()

        log_level = getattr(logging, level, logging.INFO)
        
        # Make log level consistent across all uvm objects
        uvm_report_object.set_default_logging_level(log_level)
        
        super().__init__(name, parent)
    
    def build_phase(self):
        super().build_phase()
        
        self.dut: SimHandleBase = cocotb.top
        
        self.env: gpio_env = gpio_env.create(name="env", parent=self)
        
        
    def connect_phase(self):
        super().connect_phase()
        
        
    def end_of_elaboration_phase(self):
        super().end_of_elaboration_phase()
        
        
    def start_of_simulation_phase(self):
        super().start_of_simulation_phase()
        
        
    async def run_phase(self):
        await super().run_phase()
        
        self.raise_objection()
        
        cocotb.start_soon(Clock(self.dut.clk, 10, units='ns').start())
        self.logger.debug("System Clock started")
        
        self.dut.rst.value = 0
        await ClockCycles(self.dut.clk, 10)
        self.dut.rst.value = 1
        self.logger.debug("System wide reset done")
        
        self.drop_objection()
        
        
    def extract_phase(self):
        super().extract_phase()
        

    def check_phase(self):
        super().check_phase()
        

    def report_phase(self):
        super().report_phase()
        

    def final_phase(self):
        super().final_phase()
