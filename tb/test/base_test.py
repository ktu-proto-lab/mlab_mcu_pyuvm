import cocotb
import logging
import os
from cocotb.handle import SimHandleBase
from pyuvm import uvm_test, uvm_report_object

class BaseTest(uvm_test):
    def __init__(self, name="BaseTest", parent=None):
        level: str = os.getenv(key="PYUVM_LOG_LEVEL", default="INFO").upper()
        log_level = getattr(logging, level, logging.INFO)
        uvm_report_object.set_default_logging_level(log_level)
        super().__init__(name, parent)
        self.dut: SimHandleBase = None

    def build_phase(self):
        super().build_phase()
        self.dut = cocotb.top

    def connect_phase(self):
        super().connect_phase()

    def end_of_elaboration_phase(self):
        super().end_of_elaboration_phase()

    def start_of_simulation_phase(self):
        super().start_of_simulation_phase()

    async def run_phase(self):
        self.raise_objection()
        await super().run_phase()
        self.drop_objection()

    def extract_phase(self):
        super().extract_phase()

    def check_phase(self):
        super().check_phase()

    def report_phase(self):
        super().report_phase()

    def final_phase(self):
        super().final_phase()
