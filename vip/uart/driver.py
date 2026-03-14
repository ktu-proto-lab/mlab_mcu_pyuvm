from pyuvm import uvm_driver, ConfigDB, uvm_analysis_port, uvm_not_implemeneted
from vip.uart.vif import uart_if

class uart_driver(uvm_driver):
    def build_phase(self):
        super().build_phase()

        self.vif: uart_if = ConfigDB().get(context=self, inst_name="", field_name="vif")
        
        self.analysis_port = uvm_analysis_port(name="analysis_port", parent=self)
        
    async def run_phase(self):
        await super().run_phase()
        
        self.vif.enable_transmit()

        while True:
            
            item = await self.seq_item_port.get_next_item()
            
            self.logger.info(f"driving: {item}")

            await self.vif.transmit_byte(item.byte)
            
            self.seq_item_port.item_done()
            
    