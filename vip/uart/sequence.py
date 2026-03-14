from pyuvm import uvm_sequence
from vip.uart.sequence_item import uart_sequence_item

class uart_string_sequence(uvm_sequence):
    def __init__(self, name="uart_string_sequence", string=""):
        super().__init__(name)

        self.string = string

    async def body(self):
        for char in self.string:
            item = uart_sequence_item("item", ord(char))
            
            await self.start_item(item)

            await self.finish_item(item)

    def __str__(self) -> str:
        return self.string