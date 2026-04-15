class TestError(Exception):
    """ Base exception for verification errors """
    pass

class NotImplementedTestError(TestError):
    pass

class ConfigTestError(TestError):
    """ Exception for configurational errors """
    pass

class VirtualInterfaceTestError(TestError):
    """ Exception for not assigned virtual interfaces or other """
    pass

class AsciiTestError(TestError):
    """ Exception for ASCII related errors where a byte value is not in rage of 0 and 127"""
    pass

class SequenceTestError(TestError):
    """ Exception related with sequences """
    pass

class CommandUnknownTestError(TestError):
    pass

class MemoryInvalidAddrTestError(TestError):
    pass

class McuCliTestError(TestError):
    """ Base exception for mcu cli related errors """
    pass

class McuCliWrongCmdStringTestError(McuCliTestError):
    pass

class McuCliCmdNotExacutableTestError(McuCliTestError):
    pass
