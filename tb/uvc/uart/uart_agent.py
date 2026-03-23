from pyuvm import uvm_agent, uvm_sequencer, uvm_analysis_port
from uvc.uart.uart_driver import uart_driver
from uvc.uart.uart_monitor import uart_monitor

class uart_agent(uvm_agent):
    
    sequencer: uvm_sequencer
    driver: uart_driver
    monitor: uart_monitor
    
    def build_phase(self):
        self.sequencer: uvm_sequencer = uvm_sequencer.create(name="sequencer", parent=self)
        self.driver: uart_driver = uart_driver.create(name="driver", parent=self)
        self.monitor: uart_monitor = uart_monitor.create(name="monitor", parent=self)
        self.receive_analysis_port: uvm_analysis_port = uvm_analysis_port.create("receive_analysis_port", self)

    def connect_phase(self):
        self.driver.seq_item_port.connect(self.sequencer.seq_item_export)
        self.monitor.analysis_port.connect(self.receive_analysis_port)