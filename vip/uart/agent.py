from pyuvm import uvm_agent, uvm_sequencer
from vip.uart.driver import uart_driver
from vip.uart.monitor import uart_monitor

class uart_agent(uvm_agent):
    
    sequencer: uvm_sequencer
    driver: uart_driver
    monitor: uart_monitor
    
    def build_phase(self):
        self.sequencer = uvm_sequencer.create(name="sequencer", parent=self)
        self.driver = uart_driver.create(name="driver", parent=self)
        self.monitor = uart_monitor.create(name="monitor", parent=self)

    def connect_phase(self):
        self.driver.seq_item_port.connect(self.sequencer.seq_item_export)
