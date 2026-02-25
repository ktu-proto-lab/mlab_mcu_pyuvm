import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, ReadOnly
from pyuvm import *
from vif.gpio import gpio
from agent.gpio.gpio_agent import gpio_agent

class gpio_env(uvm_env):
    def build_phase(self):
        self.dut = cocotb.top

        self.vif = gpio(self.dut)

        self.agent = gpio_agent(name="agent", parent=self)

        # Make GPIO's Virtual Interface and the DUT itself visible to all child components with "*"
        ConfigDB().set(context=self, inst_name="*", field_name="vif", value=self.vif)
        ConfigDB().set(self, "*", "dut", self.dut)


    async def run_phase(self):
        self.raise_objection()

        cocotb.start_soon(Clock(self.dut.clk, 1, units='ns').start())
        
        self.dut.rst.value = 0
        await ClockCycles(self.dut.clk, 10)
        self.dut.rst.value = 1

        self.drop_objection()