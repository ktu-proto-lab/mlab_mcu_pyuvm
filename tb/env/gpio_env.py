import cocotb
from pyuvm import *
from vip.gpio.gpio_vif import gpio_if
from vip.gpio.gpio_agent import gpio_agent
from tb.env.gpio_scoreboard import gpio_mirror_scoreboard

class gpio_env(uvm_env):
    def build_phase(self):
        self.dut = cocotb.top

        self.vif = gpio_if(self.dut)

        self.agent = gpio_agent(name="agent", parent=self)
        
        self.scoreboard = gpio_mirror_scoreboard(name="scoreboard", parent=self)

        # Make GPIO's Virtual Interface visible to all child components with "*"
        ConfigDB().set(context=self, inst_name="*", field_name="vif", value=self.vif)

    def connect_phase(self):
        self.agent.input_analysis_port.connect(self.scoreboard.input_fifo.analysis_export)
        self.agent.output_analysis_port.connect(self.scoreboard.output_fifo.analysis_export)
