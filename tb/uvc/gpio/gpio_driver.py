from pyuvm import *
from uvc.gpio.gpio_if import gpio_if
from uvc.gpio.gpio_sequence_item import gpio_sequence_item
from uvc.gpio.gpio_driver_config import gpio_driver_config

class gpio_driver(uvm_driver):
    cfg: gpio_driver_config
    vif: gpio_if
    analysis_port: uvm_analysis_port
    mask: int
    
    def build_phase(self):
        super().build_phase()
        
        self.cfg = ConfigDB().get(self, "", "cfg")

        self.vif = self.cfg.vif

        self.mask = self.cfg.mask
        
        self.analysis_port = uvm_analysis_port(name="analysis_port", parent=self)
        
    async def run_phase(self):
        await super().run_phase()

        while True:
            item: gpio_sequence_item = await self.seq_item_port.get_next_item()
            self.vif.drive_input(item.value, self.mask)
            self.logger.debug(f"drove {hex(item.value)}")
            
            self.analysis_port.write(item)
            await self.vif.system_clock_cycles(1000)
            self.seq_item_port.item_done()
