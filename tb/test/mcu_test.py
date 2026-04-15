import cocotb
import pyuvm
import logging
import os
from cocotb.clock import Clock
from cocotb.triggers import ReadOnly, ReadWrite, ClockCycles
from pyuvm import uvm_test, uvm_report_object, ConfigDB

from env import McuConfig, McuEnv
from vif import McuVirtualInterface

@pyuvm.test()
class McuTest(uvm_test):
    def __init__(self, name="Test", parent=None):
        level: str = os.getenv(key="PYUVM_LOG_LEVEL", default="INFO").upper()
        log_level = getattr(logging, level, logging.INFO)
        uvm_report_object.set_default_logging_level(log_level)
        super().__init__(name, parent)
        self.vif: McuVirtualInterface = None
        self.cfg: McuConfig = None
        self.env: McuEnv = None

    def build_phase(self):
        super().build_phase()

        self.vif = McuVirtualInterface()
        self.vif.wire_to_dut(dut=cocotb.top)
        self.logger.debug("virtual interface wired to the dut")

        self.cfg = McuConfig.create("cfg")
        self.cfg.vif = self.vif
        self.cfg.gpio_cfg.vif = self.vif
        self.cfg.uart_cfg.vif = self.vif

        # 'MCU_TEST_SW_DIR' is defined in the sim/makefile
        self.cfg.mem_path: str = f"{os.getenv("MCU_TEST_SW_DIR")}/"

        ConfigDB().set(self, "env", "cfg", self.cfg)
        self.env = McuEnv.create("env", self)

    def connect_phase(self):
        super().connect_phase()

    def end_of_elaboration_phase(self):
        super().end_of_elaboration_phase()

    def start_of_simulation_phase(self):
        super().start_of_simulation_phase()

    async def run_phase(self):
        self.raise_objection()
        await super().run_phase()
        self.vif.init_signal_values()
        self.logger.debug("initialized signal values")
        self.logger.debug("releasing system clock")
        self.logger.info(f"system clock: {self.vif.clock_period}{self.vif.clock_units}")
        cocotb.start_soon(Clock(self.vif.clock, self.vif.clock_period, self.vif.clock_units).start())
        self.logger.info(f"system reset for {self.vif.reset_duration} clock cycles")
        await ReadOnly()
        assert self.vif.reset.value == 0, "expected reset low"
        await ReadWrite()
        self.vif.reset.value = 0
        await ClockCycles(self.vif.clock, self.vif.reset_duration)
        self.vif.reset.value = 1
        await ReadOnly()
        assert self.vif.reset.value == 1, "expected reset high"
        self.drop_objection()

    def extract_phase(self):
        super().extract_phase()

    def check_phase(self):
        super().check_phase()

    def report_phase(self):
        super().report_phase()

    def final_phase(self):
        super().final_phase()
