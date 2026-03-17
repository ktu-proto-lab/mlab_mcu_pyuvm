from pyuvm import *
from uvc.gpio.gpio_driver import gpio_driver
from uvc.gpio.gpio_input_monitor import gpio_input_monitor
from uvc.gpio.gpio_output_monitor import gpio_output_monitor

class gpio_agent(uvm_agent):
    def build_phase(self):
        super().build_phase()

        self.sequencer = uvm_sequencer(name="sequencer", parent=self)

        self.driver = gpio_driver(name="driver", parent=self)

        self.input_monitor = gpio_input_monitor(name="input_monitor", parent=self)
        self.output_monitor = gpio_output_monitor(name="output_monitor", parent=self)
        
        self.input_analysis_port = uvm_analysis_port(name="input_analysis_port", parent=self)
        self.output_analysis_port = uvm_analysis_port(name="output_analysis_port", parent=self)
        

    def connect_phase(self):
        super().connect_phase()

        # Connect Driver to the Sequencer
        self.driver.seq_item_port.connect(self.sequencer.seq_item_export)
        
        # Connect Driver to the Input Monitor for monitoring correct input values
        self.driver.analysis_port.connect(self.input_monitor.driver_fifo.analysis_export)

        # Export Monitoring analysis ports to the Agent's boundary
        self.input_monitor.analysis_port.connect(self.input_analysis_port)
        self.output_monitor.analysis_port.connect(self.output_analysis_port)