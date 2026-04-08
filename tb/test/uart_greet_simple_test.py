import pyuvm
from pyuvm import uvm_tlm_analysis_fifo
from test.mcu_base_test import McuBaseTest
from uvc.uart import UartTransaction
from seq import UartStringSequence

@pyuvm.test()
class UartGreetSimpleTest(McuBaseTest):
    def __init__(self, name="UartGreetSimpleTest", parent=None):
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
        self.logger.debug("connected uart monitor to fifo")
        self.logger.debug("connect phase done")

    async def receive_string_buffer(self, length: int) -> str:
        string = ""
        for _ in range(length):
            txn: UartTransaction = await self.fifo.get()
            string += chr(txn.byte)
        return string

    async def run_phase(self):
        self.raise_objection()
        self.logger.debug("raising the objection")
        await super().run_phase()
        expected_string = "hello uart"
        self.logger.info(f"waiting to receive '{expected_string}'")
        received_string = await self.receive_string_buffer(len(expected_string))
        self.logger.info(f"received: '{received_string}'")
        assert received_string == expected_string, f"expected '{expected_string}', got '{received_string}'"
        await self.uart_if.enable_transmit()
        self.logger.info("enabled transmittion to the mcu")
        transmit_string = "hello back"
        transmit_string_sequence: UartStringSequence = UartStringSequence.create("transmit_string")
        transmit_string_sequence.string = transmit_string
        self.logger.info(f"transmitting '{transmit_string}' to mcu")
        await transmit_string_sequence.start(self.env.uart.sequencer)
        await self.uart_if.disable_transmit()
        self.logger.info(f"transmitted '{transmit_string}'")
        self.fifo.flush() # ignore garbage values if any recorded while transmitting to dut
        self.logger.debug("fifo flushed")
        first_item: UartTransaction = await self.fifo.get()
        first_char = chr(first_item.byte)
        success_response_string = "roger that"
        received_sucess_string = False
        error_response_string = "error: bad msg"
        if first_char == "r":
            received_sucess_string = True
            rest = await self.receive_string_buffer(len(success_response_string) - 1)
            response_string = first_char + rest
        else:
            rest = await self.receive_string_buffer(len(error_response_string) - 1)
            response_string = first_char + rest
        self.logger.info(f"received response: '{response_string}'")
        if received_sucess_string:
            assert (response_string == success_response_string
                ),(f"expected='{success_response_string}', actual='{response_string}'")
            self.logger.info("received expected success string")
        else:
            # TODO: failure must be reported, maybe fail the test?
            assert (response_string == error_response_string
                ),(f"expected='{error_response_string}', actual='{response_string}'")
            self.logger.info("received expected error string")
        self.logger.debug("run phase over, dropping the objection")
        self.drop_objection()
