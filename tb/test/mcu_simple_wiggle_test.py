import pyuvm
from test.mcu_base_test import mcu_base_test
from seq import gpio_sequence

@pyuvm.test()
class mcu_simple_wiggle_test(mcu_base_test):
    def build_phase(self):
        super().build_phase()
        self.cfg.uart_enable = False
    
    async def run_phase(self):
        self.raise_objection()
        await super().run_phase()
        sequence: gpio_sequence = gpio_sequence.create("sequence")
        await sequence.start(self.env.gpio_agent.sequencer)
        self.drop_objection()