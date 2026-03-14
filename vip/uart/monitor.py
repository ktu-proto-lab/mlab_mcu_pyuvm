from cocotb.triggers import RisingEdge, ReadOnly
from pyuvm import uvm_monitor, uvm_analysis_port, ConfigDB
from vip.uart.vif import uart_if
from vip.uart.sequence_item import uart_sequence_item

class uart_monitor(uvm_monitor):
    def build_phase(self):
        self.vif: uart_if = ConfigDB().get(self, "", "vif")
        
        self.analysis_port = uvm_analysis_port("analysis_port", self)

    async def run_phase(self):
        
        await self.vif.wait_receive_enable()
        
        while True:
            
            await self.vif.wait_receive_enable()
            
            self.logger.debug("receive enabled, starting monitoring uart output")
            
            if not self.vif.receive_enable():
                continue
            
            self.logger.debug("receiving byte")
            byte: int = await self.vif.receive_byte()
            self.logger.debug(f"byte received {hex(byte)}")
            
            if not self.vif.receive_enable():
                continue
            
            item = uart_sequence_item("rx_item", byte)
            
            self.logger.info(f"monitored: {item}")

            self.analysis_port.write(item)