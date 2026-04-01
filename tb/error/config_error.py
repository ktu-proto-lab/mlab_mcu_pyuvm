from pyuvm import uvm_env

class config_error(Exception):
    """ Base exception for configurational errors """
    pass

class env_config_error(config_error):
    def __init__(self, message: str, parent: uvm_env):
        parent.logger.error(message)