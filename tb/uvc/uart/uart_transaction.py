from pyuvm import uvm_sequence_item
from error import UartAsciiError

class UartTransaction(uvm_sequence_item):
    def __init__(self, name="uart_transaction", byte: int = 0xFF):
        super().__init__(name)
        self.byte = byte

    def char_value(self) -> chr:
        return chr(self.byte)

    def hex_value(self) -> str:
        return hex(self.byte)

    def bin_value(self) -> str:
        return bin(self.byte)

    def is_null_terminator(self) -> bool:
        return self.byte == 0x00

    def __str__(self) -> str:
        return f"{hex(self.byte)}"

    def __eq__(self, other) -> bool:
        return type(self) == type(other) and self.byte == other.byte

    def do_copy(self, rhs):
        self.byte = rhs.byte
        
    def is_idle_byte(self) -> bool:
        return self.byte == 0xff
        
    def to_ascii(self) -> chr:
        if self.byte < 0 or self.byte > 127:
            raise UartAsciiError(f"byte {self.hex_value()} can not be converted to ascci character")
        return chr(self.byte)
