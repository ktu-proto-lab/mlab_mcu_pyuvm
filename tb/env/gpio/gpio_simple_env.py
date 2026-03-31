from pyuvm import uvm_env, ConfigDB
from uvc.gpio import gpio_config, gpio_agent, gpio_if, gpio_monitor_config, gpio_driver_config
from env.gpio.gpio_simple_env_config import gpio_simple_env_config
from env.gpio.gpio_simple_scoreboard import gpio_simple_scoreboard

class gpio_simple_env(uvm_env):
    
    cfg: gpio_simple_env_config
    vif: gpio_if
    
    def build_phase(self):

        if not ConfigDB().exists(self, "", "cfg"):
            self.logger.error("can not build environment, configuration not provided")
            
        self.cfg = ConfigDB().get(self, "", "cfg")
        
        self.vif = self.cfg.vif
        
        input_agent_cfg: gpio_config = gpio_config.create("input_agent_cfg")
        input_agent_cfg.vif = self.vif
        input_agent_cfg.port_type = gpio_config.port_type_enum.INPUT
        input_agent_cfg.is_active = True
        input_agent_cfg.monitor_cfg = gpio_monitor_config.create("input_monitor_cfg")
        input_agent_cfg.monitor_cfg.mask = self.cfg.input_mask
        input_agent_cfg.driver_cfg = gpio_driver_config.create("input_driver_cfg")
        input_agent_cfg.driver_cfg.mask = self.cfg.input_mask
        ConfigDB().set(self, "input_agent", "cfg", input_agent_cfg)
        self.input_agent: gpio_agent = gpio_agent.create("input_agent", self)
        
        output_agent_cfg: gpio_config = gpio_config.create("output_agent_cfg")
        output_agent_cfg.vif = self.vif
        output_agent_cfg.port_type = gpio_config.port_type_enum.OUTPUT
        output_agent_cfg.is_active = False
        output_agent_cfg.monitor_cfg = gpio_monitor_config.create("output_monitor_cfg")
        output_agent_cfg.monitor_cfg.mask = self.cfg.output_mask
        ConfigDB().set(self, "output_agent", "cfg", output_agent_cfg)
        self.output_agent: gpio_agent = gpio_agent.create("output_agent", self)
        
        self.scoreboard = gpio_simple_scoreboard(name="scoreboard", parent=self)

        ConfigDB().set(context=self, inst_name="*", field_name="vif", value=self.vif)

    def connect_phase(self):
        self.input_agent.analysis_port.connect(self.scoreboard.input_fifo.analysis_export)
        self.output_agent.analysis_port.connect(self.scoreboard.output_fifo.analysis_export)
