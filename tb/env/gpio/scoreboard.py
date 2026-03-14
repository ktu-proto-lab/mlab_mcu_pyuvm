from pyuvm import *
from vip.gpio.ref_model import gpio_mirror_ref_model
from vip.gpio.sequence_item import gpio_sequence_item

class gpio_mirror_scoreboard(uvm_component):

    def build_phase(self):
        super().build_phase()

        self.model = gpio_mirror_ref_model()

        self.input_fifo = uvm_tlm_analysis_fifo("input_fifo", self)
        self.output_fifo  = uvm_tlm_analysis_fifo("output_fifo", self)
        
        self.failure: int = 0
        self.tr_count: int = 0

    async def run_phase(self):
        await super().run_phase()
        
        while True:
            input_tr: gpio_sequence_item = await self.input_fifo.get()
            
            self.logger.debug(f"got input: {input_tr}")
            
            output_tr: gpio_sequence_item  = await self.output_fifo.get()
            
            self.logger.debug(f"got output: {output_tr}")
            
            expected = self.model.predict(input_tr.value)
            actual   = int(output_tr.value)

            if expected == actual:
                self.logger.info(f"PASS: expected {hex(expected)}, actual = {hex(actual)}")
            else:
                self.failure += 1
                self.logger.error(f"FAIL: expected {hex(expected)}, actual = {hex(actual)}")
                
            self.tr_count += 1
            
    def report_phase(self):
        super().report_phase()
        
        assert self.tr_count > 0, f"Scoreboard did not receive any transactions!"
