from pyuvm import uvm_sequencer

class gpio_sequencer(uvm_sequencer):
    def build_phase(self):
        super().build_phase()
