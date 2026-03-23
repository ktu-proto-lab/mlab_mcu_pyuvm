from cocotb.triggers import RisingEdge, ReadOnly
from pyuvm import uvm_monitor, uvm_analysis_port, ConfigDB
from typing import cast
from uvc.uart.uart_if import uart_if
from uvc.uart.uart_char_item import uart_char_item

class uart_monitor(uvm_monitor):
    
    vif: uart_if
    analysis_port: uvm_analysis_port
    
    def build_phase(self):
        super().build_phase()
        
        self.vif = cast(uart_if, ConfigDB().get(context=self, inst_name="", field_name="vif"))
        self.analysis_port = uvm_analysis_port(name="analysis_port", parent=self)

    async def run_phase(self):
        await super().run_phase()
        
        while True:
            received_byte: int = await self.vif.receive_byte()
            item = uart_char_item("received_item", received_byte)
            self.logger.debug(f"{item}")
            self.analysis_port.write(item)
