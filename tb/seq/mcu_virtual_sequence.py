from pyuvm import uvm_sequence

from errors import SequenceTestError
from env import McuVirtualSequencer

class McuVirtualSequence(uvm_sequence):
    _no_event_pool_warned = False

    def __init__(self, name="McuVirtualSequence"):
        super().__init__(name)
        self.sequencer: McuVirtualSequencer = None

    async def body(self):
        await super().body()

        if self.sequencer is None:
            raise SequenceTestError("no provided sequencer")

        if not isinstance(self.sequencer, McuVirtualSequencer):
            raise TypeError(f"virtual sequence expects sequencer to be VirtualSequencer type, but is provided with {type(self.sequencer).__name__}")

        if self.sequencer.event_pool is None and not self._no_event_pool_warned:
            self.sequencer.logger.warning("some of virtual sequences rely on event pool for synchronization, virtual sequencer has none")
            _no_event_pool_warned = True
