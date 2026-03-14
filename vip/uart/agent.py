from pyuvm import uvm_agent, uvm_sequencer
from vip.uart.driver import uart_driver
from vip.uart.monitor import uart_monitor

class uart_agent(uvm_agent):
    def build_phase(self):
        self.sequencer = uvm_sequencer("sequencer", self)
        
        self.driver = uart_driver("driver", self)

        self.monitor = uart_monitor("monitor", self)

    def connect_phase(self):
        self.driver.seq_item_port.connect(self.sequencer.seq_item_export)
