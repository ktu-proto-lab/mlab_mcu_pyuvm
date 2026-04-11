class Error(Exception):
    """ Base exception for verification errors """
    pass       

class ConfigError(Error):
    """ Exception for configurational errors """
    pass

class VirtualInterfaceError(Error):
    """ Exception for not assigned virtual interfaces or other """
    pass

class AsciiError(Error):
    """ Exception for ASCII related errors where a byte value is not in rage of 0 and 127"""
    pass