from pyuvm import uvm_sequence
from uvc.uart import UartTransaction

class UartStringSequence(uvm_sequence):
    def __init__(self, name="UartStringSequence", string=""):
        super().__init__(name)
        self.string = string

    async def body(self):
        txn: UartTransaction = None
        for char in self.string:
            txn = UartTransaction.create("txn")
            txn.byte = ord(char)
            await self.start_item(txn)
            await self.finish_item(txn)

    def __str__(self) -> str:
        return self.string
