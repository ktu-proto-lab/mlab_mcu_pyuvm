from pyuvm import uvm_sequence
from uvc import UartByte

class UartStringSequence(uvm_sequence):
    def __init__(self, name="UartStringSequence", string=""):
        super().__init__(name)
        self.string = string

    def set_string(self, string):
        self.string = f"{string}\0"

    async def body(self):
        byte: UartByte = None
        for char in self.string:
            byte = UartByte.create("txn")
            byte.val = ord(char)
            await self.start_item(byte)
            await self.finish_item(byte)

    def __str__(self) -> str:
        return self.string
