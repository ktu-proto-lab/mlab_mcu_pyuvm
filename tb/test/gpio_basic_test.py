import pyuvm
from pyuvm import *
from tb.env.gpio_env import gpio_env
from vip.gpio.gpio_sequence_item import gpio_seq_item

@pyuvm.test()
class gpio_basic_test(uvm_test):
    def build_phase(self):
        self.env = gpio_env(name="env", parent=self)

        self.fifo = uvm_tlm_analysis_fifo(name="fifo", parent=self)

    def connect_phase(self):
        self.env.agent.monitor.ap.connect(self.fifo.analysis_export)

    async def run_phase(self):
        self.raise_objection()

        expected = gpio_seq_item("", 1)

        while True:
            tr: gpio_seq_item = await self.fifo.get()

            if tr == expected:
                self.logger.info(f"PASS: GPIO_PIN_0 is high, expected = {expected.value}, actual = {tr.value}")
                break

        self.drop_objection()