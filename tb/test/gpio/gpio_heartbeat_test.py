import pyuvm
from pyuvm import uvm_tlm_analysis_fifo
from tb.test.gpio.gpio_base_test import gpio_base_test
from vip.gpio.gpio_sequence_item import gpio_sequence_item

@pyuvm.test()
# NOTE: still in refac state
class gpio_heartbeat_test(gpio_base_test):
    def build_phase(self):
        super().build_phase()
        
        self.fifo = uvm_tlm_analysis_fifo(name="fifo", parent=self)
        
    def connect_phase(self):
        self.env.agent.monitor.ap.connect(self.fifo.analysis_export)

    async def run_phase(self):
        self.raise_objection()

        expected = gpio_sequence_item("", 1)

        while True:
            tr: gpio_sequence_item = await self.fifo.get()

            if tr == expected:
                self.logger.info(f"PASS: GPIO_PIN_0 is high, expected = {expected.value}, actual = {tr.value}")
                break

        self.drop_objection()
