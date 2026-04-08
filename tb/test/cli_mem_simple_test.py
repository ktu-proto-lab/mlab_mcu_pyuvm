import pyuvm
from pyuvm import uvm_tlm_analysis_fifo
from test.mcu_base_test import McuBaseTest
from seq import CliMemSequence

@pyuvm.test()
class CliMemSimpleTest(McuBaseTest):
    def __init__(self, name="CliCmdEchoSimpleTest", parent=None):
        super().__init__(name, parent)
        self.uart_receive_fifo: uvm_tlm_analysis_fifo = None

    def build_phase(self):
        super().build_phase()
        self.env_cfg.gpio.is_active = False
        self.uart_receive_fifo = uvm_tlm_analysis_fifo.create("uart_receive_fifo", self)
        self.logger.debug("build phase done")
        
    def connect_phase(self):
        super().connect_phase()
        self.env.uart.receive_analysis_port.connect(self.uart_receive_fifo.analysis_export)

    async def run_phase(self):
        self.raise_objection()
        self.logger.debug("raising the objection")
        await super().run_phase()
        sequence: CliMemSequence = CliMemSequence.create("sequence")
        sequence.uart_receive_fifo = self.uart_receive_fifo
        await sequence.start(self.env.virtual_sequencer)
        self.logger.debug("dropping the objection")
        self.drop_objection()
