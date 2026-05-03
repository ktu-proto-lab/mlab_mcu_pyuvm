from pyuvm import uvm_sequence_item

from errors import AsciiTestError

class UartByte(uvm_sequence_item):
    def __init__(self, name="UartByte", byte: int = 0x00):
        super().__init__(name)
        self.val = byte

    def __str__(self):
        return hex(self.val)

    def is_idle_byte(self) -> bool:
        return self.val == 0xff

    def to_hex(self) -> str:
        return hex(self.val)

    def to_ascii(self) -> chr:
        if self.val < 0 or self.val > 127:
            raise AsciiTestError(f"byte {self.to_hex()} can not be converted to ascii character")
        return chr(self.val)
