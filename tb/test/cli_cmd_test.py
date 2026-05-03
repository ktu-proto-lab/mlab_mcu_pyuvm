import pyuvm

from seq.cli_cmd_sequence import CliCmdSequence
from test.mcu_test import McuTest

@pyuvm.test()
class CliCmdTest(McuTest):
    def __init__(self, name="CliCmdTest", parent=None):
        super().__init__(name, parent)

    async def run_phase(self):
        self.raise_objection()
        await super().run_phase()
        seq: CliCmdSequence = CliCmdSequence.create("sequence")
        await seq.start(self.env.virtual_sequencer)
        self.drop_objection()
