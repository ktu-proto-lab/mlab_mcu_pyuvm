import cocotb
from pyuvm import uvm_env, ConfigDB
from uvc.gpio import gpio_config, gpio_agent, gpio_if
from env.gpio.gpio_scoreboard import gpio_scoreboard

class gpio_env(uvm_env):
    def build_phase(self):
        self.dut = cocotb.top

        self.vif = gpio_if(self.dut)
        
        input_agent_cfg: gpio_config = gpio_config.create("input_agent_cfg")
        input_agent_cfg.vif = self.vif
        input_agent_cfg.port_type = gpio_config.port_type_enum.INPUT
        input_agent_cfg.is_active = True
        ConfigDB().set(self, "input_agent", "cfg", input_agent_cfg)
        self.input_agent: gpio_agent = gpio_agent.create("input_agent", self)
        
        output_agent_cfg: gpio_config = gpio_config.create("output_agent_cfg")
        output_agent_cfg.vif = self.vif
        output_agent_cfg.port_type = gpio_config.port_type_enum.OUTPUT
        output_agent_cfg.is_active = False
        ConfigDB().set(self, "output_agent", "cfg", output_agent_cfg)
        self.output_agent: gpio_agent = gpio_agent.create("output_agent", self)
        
        self.scoreboard = gpio_scoreboard(name="scoreboard", parent=self)

        ConfigDB().set(context=self, inst_name="*", field_name="vif", value=self.vif)

    def connect_phase(self):
        self.input_agent.analysis_port.connect(self.scoreboard.input_fifo.analysis_export)
        self.output_agent.analysis_port.connect(self.scoreboard.output_fifo.analysis_export)
