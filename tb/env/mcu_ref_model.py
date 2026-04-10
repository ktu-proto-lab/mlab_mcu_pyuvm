from pyuvm import uvm_component, uvm_analysis_port, uvm_tlm_analysis_fifo
from seq import CliMemTransaction, CliMemCmdEnum

class McuReferenceModel(uvm_component):
    def __init__(self, name="McuReferenceModel", parent=None):
        super().__init__(name, parent)
        self.input: uvm_tlm_analysis_fifo = None
        self.output: uvm_analysis_port = None

    def build_phase(self):
        super().build_phase()
        self.input = uvm_tlm_analysis_fifo.create("input", self)
        self.output = uvm_analysis_port.create("output", self)
        
    def write(self, txn: CliMemTransaction):
        # TODO (impl)
        if txn.cmd == CliMemCmdEnum.read:
            self.logger.info("read!")
        self.output.write("expected result")