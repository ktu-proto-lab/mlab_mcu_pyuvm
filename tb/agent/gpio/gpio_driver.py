from pyuvm import *
from cocotb.triggers import ClockCycles, RisingEdge
from vif.gpio_if import gpio_if
from obj.gpio_seq_item import gpio_seq_item

class gpio_driver(uvm_driver):
    def build_phase(self):
        super().build_phase()

        self.vif: gpio_if = ConfigDB().get(context=self, inst_name="", field_name="vif")
        
        self.ap = uvm_analysis_port(name="ap", parent=self)

    async def run_phase(self):
        await super().run_phase()

        while True:
            item: gpio_seq_item = await self.seq_item_port.get_next_item()

            self.vif.drive_input(item.value)
            
            self.logger.debug(f"drove {hex(item.value)}")
            
            await ClockCycles(self.vif.clk, 1000)
            
            self.ap.write(item)

            self.seq_item_port.item_done()