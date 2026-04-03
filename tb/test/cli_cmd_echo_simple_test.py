import pyuvm
from pyuvm import uvm_tlm_analysis_fifo
from test.mcu_base_test import McuBaseTest
from seq import UartStringSequence
from uvc.uart import UartTransaction

@pyuvm.test()
class CliCmdEchoSimpleTest(McuBaseTest):
    def __init__(self, name="McuBaseTest", parent=None):
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
        self.logger.debug("connect phase done")
        
    async def receive_string_buffer(self, length: int) -> str:
        while True:
            txn: UartTransaction = await self.fifo.peek()
            if txn.byte == 0x00:
                _ = await self.fifo.get()
            else:
                break
        string = ""
        for _ in range(length):
            txn: UartTransaction = await self.fifo.get()
            string += chr(txn.byte)
        return string
        
    async def run_phase(self):
        self.raise_objection()
        self.logger.debug("raising the objection")
        await super().run_phase()
        expected_string = "ack\0"
        self.logger.info(f"waiting for dut's acknowledgement message '{expected_string}'")
        received_string = await self.receive_string_buffer(len(expected_string))
        self.logger.info(f"received message: {received_string}")
        assert (expected_string == received_string),(
            f"expected ack message '{expected_string}', received='{received_string}'"
        )
        expected_string = "mlab mcu 2026\0"
        echo_transmit_string_sequence: UartStringSequence = UartStringSequence.create("echo_sequence")
        echo_transmit_string_sequence.string = f"echo \"{expected_string}\"\0";
        self.logger.info(f"transmitting '{echo_transmit_string_sequence}'")
        self.fifo.flush()
        self.uart_if.enable_transmit()
        await echo_transmit_string_sequence.start(self.env.uart.sequencer)
        self.uart_if.disable_transmit()
        self.logger.info(f"transmitted '{echo_transmit_string_sequence}'")
        self.logger.info("waiting echo response")
        actual_received_string = await self.receive_string_buffer(len(expected_string))
        self.logger.info(f"received '{actual_received_string}'")
        assert (expected_string == actual_received_string),( 
            "echoed strings do not match: " 
            f"transmitted = {echo_transmit_string_sequence},"
            f"expected '{expected_string}', received '{actual_received_string}'"
        )
        self.logger.debug("dropping the objection")
        self.drop_objection()
