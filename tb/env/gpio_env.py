import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
from pyuvm import *
from vip.gpio.gpio_vif import gpio_if
from vip.gpio.gpio_agent import gpio_agent
from tb.env.gpio_scoreboard import gpio_mirror_scoreboard

class gpio_env(uvm_env):
    def build_phase(self):
        self.dut = cocotb.top

        self.vif = gpio_if(self.dut)

        self.agent = gpio_agent(name="agent", parent=self)
        
        self.scoreboard = gpio_mirror_scoreboard(name="sb", parent=self)

        # Make GPIO's Virtual Interface visible to all child components with "*"
        ConfigDB().set(context=self, inst_name="*", field_name="vif", value=self.vif)

    def connect_phase(self):
        self.agent.input_analysis_port.connect(self.scoreboard.stim_fifo.analysis_export)
        self.agent.output_analysis_port.connect(self.scoreboard.mon_fifo.analysis_export)


    async def run_phase(self):
        self.raise_objection()

        cocotb.start_soon(Clock(self.dut.clk, 10, units='ns').start())
        
        self.dut.rst.value = 0
        await ClockCycles(self.dut.clk, 10)
        self.dut.rst.value = 1

        self.drop_objection()