from pyuvm import uvm_sequence_item

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

    def __str__(self):
        return f"{chr(self.byte)}"

    def __eq__(self, other):
        return type(self) == type(other) and self.byte == other.byte

    def do_copy(self, rhs):
        self.byte = rhs.byte
