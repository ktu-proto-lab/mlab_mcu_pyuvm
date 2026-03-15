from pyuvm import uvm_driver, ConfigDB, uvm_analysis_port
from typing import cast
from vip.uart.sequence_item import uart_sequence_item
from vip.uart.vif import uart_vif

class uart_driver(uvm_driver):
    vif: uart_vif
    analysis_port: uvm_analysis_port
    
    def build_phase(self):
        super().build_phase()

        self.vif = cast(uart_vif, ConfigDB().get(context=self, inst_name="", field_name="vif"))
        self.analysis_port = uvm_analysis_port(name="analysis_port", parent=self)
        
    async def run_phase(self):
        await super().run_phase()
        
        while True:
            item: uart_sequence_item = await self.seq_item_port.get_next_item()
            
            self.logger.debug(f"{item}")
            await self.vif.transmit_byte(item.byte)
            self.analysis_port.write(item)
            self.seq_item_port.item_done()
    