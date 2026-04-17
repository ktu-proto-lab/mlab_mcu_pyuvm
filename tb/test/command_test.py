import pyuvm

from seq.command_sequence import CommandSequence
from test.mcu_test import McuTest

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
