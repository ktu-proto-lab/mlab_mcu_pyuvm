from pyuvm import *
from cocotb.triggers import ClockCycles
from vip.gpio.gpio_if import gpio_if
from vip.gpio.gpio_sequence_item import gpio_sequence_item

class gpio_driver(uvm_driver):
    def build_phase(self):
        super().build_phase()

        self.vif: gpio_if = ConfigDB().get(context=self, inst_name="", field_name="vif")
        
        # Report driven values directly to the Input Monitor to avoid intermediate changing values being monitored by
        # the Input Monitor
        self.analysis_port = uvm_analysis_port(name="analysis_port", parent=self)
        
    async def run_phase(self):
        await super().run_phase()

        while True:
            item: gpio_sequence_item = await self.seq_item_port.get_next_item()

            self.vif.drive_input(value=item.value, mask=0x0F)
            
            self.logger.debug(f"drove {hex(item.value)}")
            
            self.analysis_port.write(item)
            
            await ClockCycles(self.vif.clk, 1000)
            
            self.seq_item_port.item_done()