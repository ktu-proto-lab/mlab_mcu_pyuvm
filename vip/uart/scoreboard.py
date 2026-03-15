from pyuvm import uvm_scoreboard, uvm_tlm_analysis_fifo
from vip.uart.sequence_item import uart_sequence_item

class uart_scoreboard(uvm_scoreboard):
    
    receive_fifo: uvm_tlm_analysis_fifo
    transmit_fifo: uvm_tlm_analysis_fifo
    
    transaction_count: int = 0
    failure: bool = False
    
    def build_phase(self):
        super().build_phase()
        
        self.receive_fifo = uvm_tlm_analysis_fifo(name="receive_fifo", parent=self)
        self.transmit_fifo = uvm_tlm_analysis_fifo(name="transmit_fifo", parent=self)
        
    async def run_phase(self):
        await super().run_phase()

        while True:
            transmit_transaction: uart_sequence_item = await self.transmit_fifo.get()
            self.logger.debug(f"transmitted transaction {transmit_transaction}")
            
            receive_transaction: uart_sequence_item = await self.receive_fifo.get()
            self.logger.debug(f"received transaction {receive_transaction}")
            
            self.transaction_count += 1
            
    def report_phase(self):
        super().report_phase()

        assert self.transaction_count > 0, f"no received transactions"
            