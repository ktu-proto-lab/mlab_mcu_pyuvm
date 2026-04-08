from pyuvm import uvm_component

class TestError(Exception):
    """ Base exceptin for test related errors """
    def __init__(self, reason: str, parent: uvm_component):
        if parent is None:
            return
        parent.logger.error(reason)

class ConfigError(TestError):
    """ Base exception for configurational errors """
    def __init__(self, reason: str, parent: uvm_component):
        super().__init__(reason, parent)

class UartAsciiError(TestError):
    """ Exception for ASCII related errors where a byte value is not in rage of 0 and 127"""
    def __init__(self, reason: str, parent=None):
        super().__init__(reason, parent)