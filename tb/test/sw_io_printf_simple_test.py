import pyuvm
from pyuvm import uvm_tlm_analysis_fifo
from test.mcu_base_test import McuBaseTest
from uvc.uart import UartTransaction


@pyuvm.test()
class SwIoPrintfSimpleTest(McuBaseTest):
    def __init__(self, name="SwIoPrintfSimpleTest", parent=None):
        super().__init__(name, parent)
        self.fifo: uvm_tlm_analysis_fifo = None

    def build_phase(self):
        super().build_phase()
        self.env_cfg.gpio.is_active = False
        self.fifo = uvm_tlm_analysis_fifo.create("fifo", self)
        self.logger.debug("build phase done")

    def connect_phase(self):
        super().connect_phase()
        self.env.uart.monitor.analysis_port.connect(self.fifo.analysis_export)
        self.logger.debug("connected fifo to the uart monitor analysis port")
        self.logger.debug("connect phase done")

    # TODO (refac): move to utils or smth, this will be used in many tests
    async def receive_string(self) -> str:
        string = ""
        while True:
            txn: UartTransaction = await self.fifo.get()
            if txn.char_value() == '\n':
                return string
            string += txn.char_value()

    async def run_phase(self):
        self.raise_objection()
        self.logger.debug("raising the objection")
        await super().run_phase()
        expected_string= "printf: s: string, int: 189, int: -9021, uint: 1926478, int: 0, uint: 0, char: h, %r"
        self.logger.info(f"waiting to receive '{expected_string}'")
        received_string = await self.receive_string()
        assert received_string == expected_string, f"expected='{expected_string}', actual='{received_string}'"
        self.logger.info(f"received: '{received_string}'")
        expected_string = "printf: over!"
        received_string = await self.receive_string()
        assert received_string == expected_string, f"expected='{expected_string}', actual='{received_string}'"
        self.logger.info(f"received: '{received_string}'")
        self.logger.debug("dropping the objection")
        self.drop_objection()
