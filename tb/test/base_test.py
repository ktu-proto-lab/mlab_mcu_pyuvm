import cocotb
import logging
import os
from cocotb.handle import SimHandleBase
from pyuvm import uvm_test, uvm_report_object
from vif import mcu_vif

class base_test(uvm_test):    
    def __init__(self, name="base_test", parent=None):
        # let set log level from the makefile itself, default to info
        level: str = os.getenv(key="PYUVM_LOG_LEVEL", default="INFO").upper()
        log_level = getattr(logging, level, logging.INFO)
        
        # make log level consistent across all uvm objects
        uvm_report_object.set_default_logging_level(log_level)
        
        super().__init__(name, parent)
        
        self.dut: SimHandleBase = None
        self.mcu_vif: mcu_vif = None
        
    def build_phase(self):
        super().build_phase()
        self.dut = cocotb.top
        self.mcu_vif = mcu_vif(name="dut", parent=self)
        self.mcu_vif.wire(self.dut)
        
    def connect_phase(self):
        super().connect_phase()

    def end_of_elaboration_phase(self):
        super().end_of_elaboration_phase()

    def start_of_simulation_phase(self):
        super().start_of_simulation_phase()

    async def run_phase(self):
        self.raise_objection()
        await super().run_phase()

        self.mcu_vif.release_clock()
        self.logger.debug("dut clock released")
        
        await self.mcu_vif.reset_system()
        self.logger.debug("dut system-wide reset done")

        self.drop_objection()

    def extract_phase(self):
        super().extract_phase()

    def check_phase(self):
        super().check_phase()

    def report_phase(self):
        super().report_phase()

    def final_phase(self):
        super().final_phase()
