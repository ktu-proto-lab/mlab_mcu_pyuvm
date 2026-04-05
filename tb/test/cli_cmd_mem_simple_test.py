import pyuvm
from pyuvm import uvm_tlm_analysis_fifo
from test.mcu_base_test import McuBaseTest
from seq import UartStringSequence
from uvc.uart import UartTransaction

@pyuvm.test()
class CliCmdMemSimpleTest(McuBaseTest):
    def __init__(self, name="CliCmdMemSimpleTest", parent=None):
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

    async def receive_string_response(self) -> str:
        string = ""
        while True:
            txn: UartTransaction = await self.fifo.get()
            if txn.char_value() == '\n':
                return string
            if txn.is_null_terminator():
                continue
            string += txn.char_value()

    # TODO: add a console that just prints the output from the uart tx
    # The cocotb task should be used for this to continuesly monitor the output
    async def monitor_uart_transmit(self):
        string = ""


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
        expected_string = "[  DEBUG]: cmd mem read"
        cmd_mem_sequence: UartStringSequence = UartStringSequence.create("cmd_mem_sequence")
        cmd_mem_sequence.set_string("mem read 0x0000")
        self.logger.info(f"transmitting '{cmd_mem_sequence}'")
        self.fifo.flush()
        self.uart_if.enable_transmit()
        await cmd_mem_sequence.start(self.env.uart.sequencer)
        self.uart_if.disable_transmit()
        self.logger.info(f"transmitted '{cmd_mem_sequence}'")
        self.logger.info("waiting for response")
        received_string = await self.receive_string_response()
        self.logger.info(f"received '{received_string}'")
        assert expected_string == received_string, (
            "did not receive debug message from the cli",
            f"transmitted = {cmd_mem_sequence}, "
            f"expected '{expected_string}', received '{received_string}'"
        )
        self.logger.debug("dropping the objection")
        self.drop_objection()
