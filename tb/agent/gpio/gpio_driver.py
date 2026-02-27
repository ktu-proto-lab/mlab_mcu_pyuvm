from pyuvm import *
from cocotb.triggers import ClockCycles, RisingEdge
from vif.gpio import gpio
from obj.gpio_seq_item import gpio_seq_item

class gpio_driver(uvm_driver):
    def build_phase(self):
        super().build_phase()

        self.vif: gpio = ConfigDB().get(context=self, inst_name="", field_name="vif")

    async def run_phase(self):
        await super().run_phase()

        while True:
            item: gpio_seq_item = await self.seq_item_port.get_next_item()

            await ClockCycles(self.vif.clk, 500)
            await RisingEdge(self.vif.clk)
            self.vif.set_pins(int(item.value))
            
            self.logger.info(f"Driver: drove {item}")
            

            self.seq_item_port.item_done()