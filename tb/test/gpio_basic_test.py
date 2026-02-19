import pyuvm
from pyuvm import *
from env.gpio_env import gpio_env

@pyuvm.test()
class gpio_basic_test(uvm_test):
    def build_phase(self):
        self.env = gpio_env(name="env", parent=self)