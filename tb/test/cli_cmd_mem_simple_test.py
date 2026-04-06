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
            # TODO: wtf????? maybe use is_ascii or smth
            if txn.byte == 0xFF:
                continue
            if txn.char_value() == '\n':
                return string
            if txn.is_null_terminator():
                continue
            string += txn.char_value()

    # TODO: add a console that just prints the output from the uart tx
    # The cocotb task should be used for this to continuesly monitor the output
    async def monitor_uart_transmit(self):
        string = ""


    async def check_cli_cmd_mem(self, cmd_string, expected_response):
        expected_string = expected_response
        cmd_mem_sequence: UartStringSequence = UartStringSequence.create("cmd_mem_sequence")
        cmd_mem_sequence.set_string(cmd_string)
        self.logger.info(f"transmitting '{cmd_mem_sequence}'")
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
        # TODO: 6f0940 value is not checked if it is actually correct in the imem space
        await self.check_cli_cmd_mem("mem read 0x80000006", "0x6f0940")
        await self.receive_string_response()
        await self.check_cli_cmd_mem("mem write 0x80001990 0xffffffff", "0x0")
        await self.receive_string_response()
        await self.check_cli_cmd_mem("mem read 0x80001990", "0xffffffff")
        await self.receive_string_response()
        await self.check_cli_cmd_mem("mem dump <addr> [word_cnt]", "[  DEBUG]: cmd mem dump")
        await self.receive_string_response()
        await self.check_cli_cmd_mem("mem checksum <addr> [word_cnt]", "[  DEBUG]: cmd mem checksum")
        await self.receive_string_response()
        await self.check_cli_cmd_mem("mem cmd <arg1> <arg2>", "[  ERROR]: unknown mem sub-command 'cmd'")
        await self.receive_string_response()
        self.logger.debug("dropping the objection")
        self.drop_objection()
