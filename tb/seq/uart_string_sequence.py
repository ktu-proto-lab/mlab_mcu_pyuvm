from pyuvm import uvm_sequence
from uvc.uart import uart_char_item

class uart_string_sequence(uvm_sequence):
    def __init__(self, name="uart_sequence", string=""):
        super().__init__(name)

        self.string = string

    async def body(self):
        for char in self.string:
            item: uart_char_item = uart_char_item.create("item")
            item.byte = ord(char)
            await self.start_item(item)
            await self.finish_item(item)

    def __str__(self) -> str:
        return self.string