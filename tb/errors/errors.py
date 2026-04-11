class Error(Exception):
    """ Base exception for verification errors """
    pass       

class ConfigError(Error):
    """ Exception for configurational errors """
    pass

class VirtualInterfaceError(Error):
    """ Exception for not assigned virtual interfaces or other """
    pass