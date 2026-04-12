import pyuvm
from pyuvm import uvm_tlm_analysis_fifo
from seq import CommandSequence
from test import McuTest

@pyuvm.test()
class CommandTest(McuTest):
    def __init__(self, name="CommandTest", parent=None):
        super().__init__(name, parent)

    async def run_phase(self):
        self.raise_objection()
        await super().run_phase()
        seq: CommandSequence = CommandSequence.create("sequence")
        await seq.start(self.env.virtual_sequencer)
        self.drop_objection()
