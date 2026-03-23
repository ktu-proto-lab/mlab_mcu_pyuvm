from uvc.uart.uart_sequence_item import uart_sequence_item

class uart_char_item(uart_sequence_item):
    NULL_TERMINATOR = 0x00
    
    def __init__(self, name="uart_char_item", byte: int = NULL_TERMINATOR):
        super().__init__(name)    

        self.byte: int = byte
    
    def is_null_terminator(self) -> bool:
        return self.byte == self.NULL_TERMINATOR

    def __str__(self):
        return f"{chr(self.byte)}"