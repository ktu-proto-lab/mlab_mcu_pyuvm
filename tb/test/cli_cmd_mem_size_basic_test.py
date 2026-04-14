import pyuvm
from seq import CliCmdMemSizeBasicSeq
from test import McuTest

@pyuvm.test()
class CliCmdMemSizeBasicTest(McuTest):
    def __init__(self, name="CliCmdMemSizeBasicTest", parent=None):
        super().__init__(name, parent)

    async def run_phase(self):
        self.raise_objection()
        await super().run_phase()
        seq = CliCmdMemSizeBasicSeq.create("seq")
        await seq.start(self.env.virtual_sequencer)
        self.drop_objection()
