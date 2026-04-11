import pyuvm
from pyuvm import uvm_tlm_analysis_fifo
from seq import CommandSequence
from test.test import Test

@pyuvm.test()
class CommandTest(Test):
    def __init__(self, name="CommandTest", parent=None):
        super().__init__(name, parent)
        self.uart_receive_fifo: uvm_tlm_analysis_fifo = None

    def build_phase(self):
        super().build_phase()
        self.uart_receive_fifo = uvm_tlm_analysis_fifo.create("uart_receive_fifo", self)

    def connect_phase(self):
        super().connect_phase()
        # TODO: should be connected to the tracer
        self.env.uart.monitor.tx_ap.connect(self.uart_receive_fifo.analysis_export)

    async def run_phase(self):
        self.raise_objection()
        self.logger.debug("raising the objection")
        await super().run_phase()
        seq: CommandSequence = CommandSequence.create("sequence")
        seq.uart_receive_fifo = self.uart_receive_fifo
        await seq.start(self.env.virtual_sequencer)
        self.logger.debug("dropping the objection")
        self.drop_objection()
