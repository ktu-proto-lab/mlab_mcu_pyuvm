from tb.env.gpio_env import gpio_env
from tb.test.base import base_test

# TODO (06.03.26): check if the running program on the DUT exists.
class gpio_base_test(base_test):
    
    def build_phase(self):
        super().build_phase()
        
        self.env: gpio_env = gpio_env.create(name="env", parent=self)
        
