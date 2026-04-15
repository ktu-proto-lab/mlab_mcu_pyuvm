from pyuvm import uvm_object

class McuTransaction(uvm_object):
    def __init__(self, name='McuTransaction'):
        super().__init__(name)
        self.request: str = None
        self.actual: str = None
        self.expected: str = None

    def __str__(self):
        return f"request='{self.request}' expected='{self.expected}' actual='{self.actual}'"
