from pyuvm import *
from vip.gpio.gpio_ref_model import gpio_mirror_ref_model
from vip.gpio.gpio_sequence_item import gpio_seq_item

class gpio_mirror_scoreboard(uvm_component):

    def build_phase(self):
        super().build_phase()

        self.model = gpio_mirror_ref_model()

        self.stim_fifo = uvm_tlm_analysis_fifo("stim_fifo", self)
        self.mon_fifo  = uvm_tlm_analysis_fifo("mon_fifo", self)
        
        self.failure: int = 0

    async def run_phase(self):
        while True:
            mon_tr: gpio_seq_item  = await self.mon_fifo.get()
            stim_tr: gpio_seq_item = await self.stim_fifo.get()
            
            expected = self.model.predict(stim_tr.value)
            actual   = int(mon_tr.value)

            if expected == actual:
                self.logger.debug(f"PASS: expected {hex(expected)}, actual = {hex(actual)}")
            else:
                self.failure += 1
                self.logger.error(f"FAIL: expected {hex(expected)}, actual = {hex(actual)}")
