from pyuvm import uvm_component

class TestError(Exception):
    """ Base exceptin for test related errors """
    def __init__(self, reason: str, parent: uvm_component):
        parent.logger.error(reason)

class ConfigError(TestError):
    """ Base exception for configurational errors """
    def __init__(self, reason: str, parent: uvm_component):
        super().__init__(reason, parent)
