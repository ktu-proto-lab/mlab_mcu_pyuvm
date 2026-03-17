from pyuvm import uvm_monitor, uvm_tlm_analysis_fifo, uvm_analysis_port
from uvc.gpio.gpio_sequence_item import gpio_sequence_item

class gpio_input_monitor(uvm_monitor):
    def build_phase(self):
        super().build_phase()
        
        # Subscribe to Driver's Analysis Port instead of sampling intermediate changing values directly from hardware
        self.driver_fifo = uvm_tlm_analysis_fifo(name="driver_fifo", parent=self)
        
        # Broadcast directly to the Scoreboard
        self.analysis_port = uvm_analysis_port(name="analysis_port", parent=self)
    
    async def run_phase(self):
        await super().run_phase()
        
        while True:
            tr: gpio_sequence_item = await self.driver_fifo.get()
            self.logger.debug(f"Got input item from the driver: {tr}")
            
            # Forward Driver's input to the Scoreboard
            self.analysis_port.write(tr)