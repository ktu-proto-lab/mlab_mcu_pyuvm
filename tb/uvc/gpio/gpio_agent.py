from pyuvm import uvm_agent, uvm_analysis_port, ConfigDB
from uvc.gpio.gpio_driver import gpio_driver
from uvc.gpio.gpio_monitor import gpio_monitor
from uvc.gpio.gpio_input_monitor import gpio_input_monitor
from uvc.gpio.gpio_output_monitor import gpio_output_monitor
from uvc.gpio.gpio_agent_config import gpio_agent_config
from uvc.gpio.gpio_sequencer import gpio_sequencer

class gpio_agent(uvm_agent):
    cfg: gpio_agent_config
    monitor: gpio_monitor
    analysis_port: uvm_analysis_port
    
    def __init__(self, name, parent):
        super().__init__(name, parent)
        
        self.cfg = None
        self.monitor = None
        self.analysis_port = None
    
    def build_phase(self):
        super().build_phase()
        
        if not ConfigDB().exists(self, "", "cfg"):
            self.logger.error("can't build agent without set configuration")
        
        self.cfg: gpio_agent_config = ConfigDB().get(self, "", "cfg")
        
        self.vif = self.cfg.vif
        
        self.cfg.monitor_cfg.vif = self.vif
        
        ConfigDB().set(self, "monitor", "cfg", self.cfg.monitor_cfg)

        if self.cfg.port_type == gpio_agent_config.port_type_enum.INPUT:
            self.monitor = gpio_input_monitor.create(name="monitor", parent=self)
        
        elif self.cfg.port_type == gpio_agent_config.port_type_enum.OUTPUT:
            self.monitor = gpio_output_monitor.create(name="monitor", parent=self)
        
        else:
            self.logger.error("monitor can only be configured as input or output")
            
        if self.cfg.is_active:
            self.sequencer: gpio_sequencer = gpio_sequencer.create(name="sequencer", parent=self)
            
            self.cfg.driver_cfg.vif = self.vif
            ConfigDB().set(self, "driver", "cfg", self.cfg.driver_cfg)
            self.driver: gpio_driver = gpio_driver.create(name="driver", parent=self)
            
        self.analysis_port = uvm_analysis_port("analysis_port", self)
        

    def connect_phase(self):
        super().connect_phase()

        self.monitor.analysis_port.connect(self.analysis_port)

        if self.cfg.is_active:
            self.driver.seq_item_port.connect(self.sequencer.seq_item_export)
        