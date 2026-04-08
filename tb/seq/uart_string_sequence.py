from pyuvm import uvm_sequence
from uvc.uart import UartTransaction

class UartStringSequence(uvm_sequence):
    def __init__(self, name="UartStringSequence", string=""):
        super().__init__(name)
        self.string = string

    def set_string(self, string):
        self.string = f"{string}\0"

    async def body(self):
        txn: UartTransaction = None
        self.sequencer.logger.debug(f"sending {self.string}")
        for char in self.string:
            txn = UartTransaction.create("txn")
            txn.byte = ord(char)
            self.sequencer.logger.debug(f"start {txn} item")
            await self.start_item(txn)
            self.sequencer.logger.debug(f"finish {txn} item")
            await self.finish_item(txn)
            self.sequencer.logger.debug(f"item {txn} finished")

    def __str__(self) -> str:
        return self.string
