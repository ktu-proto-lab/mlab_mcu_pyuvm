import cocotb
from pyuvm import uvm_env, ConfigDB
from uvc.gpio import gpio_agent, gpio_if
from env.gpio.gpio_scoreboard import gpio_scoreboard

class gpio_env(uvm_env):
    def build_phase(self):
        self.dut = cocotb.top

        self.vif = gpio_if(self.dut)

        self.agent = gpio_agent(name="agent", parent=self)
        
        self.scoreboard = gpio_scoreboard(name="scoreboard", parent=self)

        # Make GPIO's Virtual Interface visible to all child components with "*"
        ConfigDB().set(context=self, inst_name="*", field_name="vif", value=self.vif)

    def connect_phase(self):
        self.agent.input_analysis_port.connect(self.scoreboard.input_fifo.analysis_export)
        self.agent.output_analysis_port.connect(self.scoreboard.output_fifo.analysis_export)
