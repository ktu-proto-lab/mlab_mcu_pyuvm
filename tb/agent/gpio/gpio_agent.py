from pyuvm import *
from agent.gpio.gpio_driver import gpio_driver
from agent.gpio.gpio_monitor import gpio_monitor
from seq.gpio.gpio_4bit_rnd_seq import gpio_4bit_rnd_seq

class gpio_agent(uvm_agent):
    def build_phase(self):
        super().build_phase()

        # TODO: add actual GPIO Sequencer
        self.seqr = uvm_sequencer(name="seqr", parent=self)

        self.driver = gpio_driver(name="driver", parent=self)

        self.monitor = gpio_monitor(name="monitor", parent=self)

    def connect_phase(self):
        super().connect_phase()

        # Connect Driver to the Sequencer
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)

        # NOTE: optional export of the Monitor's analysis port to the Agent's boundary
        # self.ap = self.monitor.ap