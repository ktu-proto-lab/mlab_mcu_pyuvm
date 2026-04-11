from pyuvm import uvm_tlm_analysis_fifo

from seq.virtual_sequence import VirtualSequence
from seq.command import Command
from seq.uart_string_sequence import UartStringSequence
from uvc import UartByte

class CommandSequence(VirtualSequence):
    def __init__(self, name="CommandSequence"):
        super().__init__(name)
        self.uart_receive_fifo: uvm_tlm_analysis_fifo = None

    # TODO: check if the uart sequencer has vif connected
    async def receive_uart_string(self):
        string = ""
        self.sequencer.logger.debug("receiving uart string")
        while True:
            txn: UartByte = await self.uart_receive_fifo.get()
            char: chr = txn.to_ascii()
            if char == '\n' or char == '\0':
                break
            string += char
        self.sequencer.logger.debug(f"received {string} uart string")
        return string

    # TODO: this is a job for gpio pins, not uart, same with ready
    async def ack(self):
        received_string = await self.receive_uart_string()
        assert received_string == "ack", f"expected acknowledgement string"

    async def ready(self):
        received_string = await self.receive_uart_string()
        assert received_string == "ready", f"expected ready string"

    async def send_uart_string(self, string: str):
        uart_string_sequence: UartStringSequence = UartStringSequence.create("uart_string_sequence")
        uart_string_sequence.set_string(string)
        self.sequencer.logger.info(f"sending {uart_string_sequence}")
        await uart_string_sequence.start(self.sequencer.uart)
        self.sequencer.logger.info(f"sent {uart_string_sequence}")


    async def body(self):
        await super().body()

        await self.ack()

        for _ in range(100):
            # TODO: refactor so that sequence does not handle protocol itself and just drives commands
            self.sequencer.logger.debug("forming command")
            cmd: Command = Command.create("req")
            self.sequencer.logger.debug("command formed")
            # await self.start_item(req)
            self.sequencer.logger.debug("randomizing command")
            cmd.randomize()
            self.sequencer.logger.debug("randomized cli mem transaction")
            # await self.finish_item(req)
            self.sequencer.logger.debug(f"sending via uart randomized command string '{cmd}'")
            await self.send_uart_string(cmd.to_string())
            self.sequencer.logger.debug(f"{cmd} sent, receiving response")
            await self.receive_uart_string()
            self.sequencer.logger.debug("waiting for mcu to be ready")
            await self.ready()
            self.sequencer.logger.debug("command item finished")
