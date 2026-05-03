import pyuvm

from test.mcu_test import McuTest

from pyuvm import uvm_sequence, uvm_subscriber
from cocotb.triggers import Timer
from seq.mcu_virtual_sequence import McuVirtualSequence
from uvc.gpio_pad import GpioPad

class GpioNibbleMirrorChecker(uvm_subscriber):
    def __init__(self, name="GpioNibbleMirrorChecker", parent=None):
        super().__init__(name, parent)
        self.req: int = None
        self.req_set: bool = False
        self.passed: bool = True
        self.txn_cnt: int = 0

    def write(self, item):
        if item.state == 0x00:
            return

        if not self.req_set:
            self.req = item.state
            self.req_set = True
            return

        resp = item.state

        lower_nibble = self.req & 0x0F
        upper_nibble = (resp & 0xF0) >> 4

        if lower_nibble != upper_nibble:
            self.passed = False
            self.logger.error(
                f"req ({hex(lower_nibble)}) != resp ({hex(upper_nibble)})"
            )
        else:
            self.logger.info(
                f"req ({hex(lower_nibble)}) = resp ({hex(upper_nibble)})"
            )

        self.req_set = False
        self.txn_cnt += 1


class GpioPadSequence(uvm_sequence):
    async def body(self):
        req = GpioPad.create("req")
        req.mask = 0x0F
        await self.start_item(req)
        req.randomize()
        self.sequencer.logger.debug(f"req ({req})")
        await self.finish_item(req)


class GpioNibbleSequence(McuVirtualSequence):
    def build_phase():
        super().build_phase()
        self.txn_cnt = None

    async def body(self):
        for _ in range(self.txn_cnt):
            await Timer(10000, units='ns')
            self.sequencer.logger.debug("starting transaction")

            seq = GpioPadSequence.create("seq")

            await seq.start(self.sequencer.gpio)

            self.sequencer.logger.debug("finished transaction")

        await Timer(10000, units='ns')

@pyuvm.test()
class GpioNibbleMirrorTest(McuTest):
    def __init__(self, name="GpioNibbleMirrorTest", parent=None):
        super().__init__(name, parent)
        self.txn_cnt = 100

    def build_phase(self):
        super().build_phase()
        self.cfg.uart_cfg.active = False
        self.cfg.active_scoreboard = False
        self.checker = GpioNibbleMirrorChecker.create("checker", self)

    def connect_phase(self):
        super().connect_phase()
        self.env.gpio.monitor.ap.connect(self.checker.analysis_export)

    async def run_phase(self):
        self.raise_objection()
        await super().run_phase()

        seq = GpioNibbleSequence.create("seq")
        seq.txn_cnt = self.txn_cnt
        await seq.start(self.env.virtual_sequencer)
        await self.cfg.event_pool.mcu_debug.wait()

        self.drop_objection()

    def report_phase(self):
        super().report_phase()
        assert self.checker.passed, "all transactions needs to be successfull"
        assert self.checker.txn_cnt == self.txn_cnt, "must check all transactions"
