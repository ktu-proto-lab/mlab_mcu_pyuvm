class McuTestError(Exception):
    """ Base exception for verification errors """
    pass

class NotImplementedTestError(McuTestError):
    pass

class ConfigTestError(McuTestError):
    """ Exception for configurational errors """
    pass

class VirtualInterfaceTestError(McuTestError):
    """ Exception for not assigned virtual interfaces or other """
    pass

class AsciiTestError(McuTestError):
    """ Exception for ASCII related errors where a byte value is not in rage of 0 and 127"""
    pass

class SequenceTestError(McuTestError):
    """ Exception related with sequences """
    pass

class CommandUnknownTestError(McuTestError):
    pass

class MemoryInvalidAddrTestError(McuTestError):
    pass

class McuCliTestError(McuTestError):
    """ Base exception for mcu cli related errors """
    pass

class McuCliWrongCmdStringTestError(McuCliTestError):
    pass

class McuCliCmdNotExacutableTestError(McuCliTestError):
    pass
