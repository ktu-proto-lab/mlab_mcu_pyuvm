import cocotb
import logging
import os
from cocotb.clock import Clock
from cocotb.handle import SimHandleBase
from cocotb.triggers import ClockCycles
from decimal import Decimal
from pyuvm import uvm_test, uvm_report_object

class base_test(uvm_test):
    def __init__(self, name="gpio_base_test", parent=None):
        # let set log level from the makefile itself, default to info
        level: str = os.getenv(key="COCOTB_LOG_LEVEL", default="INFO").upper()

        log_level = getattr(logging, level, logging.INFO)
        
        # make log level consistent across all uvm objects
        uvm_report_object.set_default_logging_level(log_level)
        
        super().__init__(name, parent)
        
    def build_phase(self):
        super().build_phase()
        
        self.dut: SimHandleBase = cocotb.top
        
        self.clock: SimHandleBase = self.dut.clk
        self.clock_period: Decimal = 12.5
        self.clock_time_step: str = 'ns'
        
        self.reset: SimHandleBase = self.dut.rst
        self.reset_duration: Decimal = 20
        
    def connect_phase(self):
        super().connect_phase()
        

    def end_of_elaboration_phase(self):
        super().end_of_elaboration_phase()
        

    def start_of_simulation_phase(self):
        super().start_of_simulation_phase()
        

    async def run_phase(self):
        await super().run_phase()
        
        # start system clock
        cocotb.start_soon(Clock(self.clock, self.clock_period, self.clock_time_step).start())
        self.logger.debug(f"system clock started with period of {self.clock_period}{self.clock_time_step}")
        
        # apply system reset
        self.reset.value = 0
        self.logger.debug(f"system wide reset for {self.reset_duration} clock cycles")
        await ClockCycles(self.clock, self.reset_duration)
        self.reset.value = 1
        self.logger.debug("system wide reset done")
        

    def extract_phase(self):
        super().extract_phase()
        

    def check_phase(self):
        super().check_phase()
        

    def report_phase(self):
        super().report_phase()
        

    def final_phase(self):
        super().final_phase()
        
