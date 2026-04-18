import pyuvm

from test.mcu_test import McuTest

from pyuvm import uvm_sequence
from cocotb.triggers import Timer
from seq.mcu_virtual_sequence import McuVirtualSequence
from uvc.gpio_pad import GpioPad

class GpioPadSequence(uvm_sequence):
    async def body(self):
        req = GpioPad.create("req")
        req.mask = 0x0F
        await self.start_item(req)
        req.randomize()
        self.sequencer.logger.debug(f"req ({req})")
        await self.finish_item(req)


class GpioNibbleSequence(McuVirtualSequence):
    async def body(self):
        for _ in range(10):
            await Timer(5000, units='ns')
            self.sequencer.logger.debug("starting transaction")

            seq = GpioPadSequence.create("seq")

            await seq.start(self.sequencer.gpio)

            self.sequencer.logger.debug("finished transaction")

        await Timer(5000, units='ns')

@pyuvm.test()
class GpioNibbleMirrorTest(McuTest):
    def __init__(self, name="GpioNibbleMirrorTest", parent=None):
        super().__init__(name, parent)

    def build_phase(self):
        super().build_phase()
        self.cfg.uart_cfg.active = False

    async def run_phase(self):
        self.raise_objection()
        await super().run_phase()
        seq = GpioNibbleSequence.create("seq")
        await seq.start(self.env.virtual_sequencer)
        await self.cfg.event_pool.mcu_debug.wait()
        self.drop_objection()
