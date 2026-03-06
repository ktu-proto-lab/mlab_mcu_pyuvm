from pyuvm import *
from vip.gpio.gpio_ref_model import gpio_mirror_ref_model
from vip.gpio.gpio_sequence_item import gpio_seq_item

class gpio_mirror_scoreboard(uvm_component):

    def build_phase(self):
        super().build_phase()

        self.model = gpio_mirror_ref_model()

        self.input_fifo = uvm_tlm_analysis_fifo("input_fifo", self)
        self.output_fifo  = uvm_tlm_analysis_fifo("output_fifo", self)
        
        self.failure: int = 0

    async def run_phase(self):
        while True:
            input: gpio_seq_item = await self.input_fifo.get()
            
            self.logger.debug(f"got input: {input}")
            
            output: gpio_seq_item  = await self.output_fifo.get()
            
            self.logger.debug(f"got output: {output}")
            
            expected = self.model.predict(input.value)
            actual   = int(output.value)

            if expected == actual:
                self.logger.info(f"PASS: expected {hex(expected)}, actual = {hex(actual)}")
            else:
                self.failure += 1
                self.logger.error(f"FAIL: expected {hex(expected)}, actual = {hex(actual)}")
