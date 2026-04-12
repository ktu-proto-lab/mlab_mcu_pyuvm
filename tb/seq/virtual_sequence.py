from pyuvm import uvm_sequence

from errors import SequenceError
from env import McuVirtualSequencer

class VirtualSequence(uvm_sequence):
    def __init__(self, name="VirtualSequence"):
        super().__init__(name)
        self.sequencer: McuVirtualSequencer = None

    async def body(self):
        await super().body()

        if self.sequencer is None:
            raise SequenceError("no provided sequencer")

        if not isinstance(self.sequencer, McuVirtualSequencer):
            raise TypeError(f"virtual sequence expects sequencer to be VirtualSequencer type, but is provided with {type(self.sequencer).__name__}")
