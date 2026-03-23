import pyuvm
from pyuvm import ConfigDB, uvm_tlm_analysis_fifo
from test import base_test
from uvc.uart import uart_if, uart_agent, uart_sequence_item
from seq import uart_string_sequence

@pyuvm.test()
class uart_simple_test(base_test):
    vif: uart_if
    agent: uart_agent
    
    monitor_fifo: uvm_tlm_analysis_fifo
    
    def __init__(self, name="gpio_base_test", parent=None):
        super().__init__(name, parent)
        
        self.vif = None
        self.agent = None
        self.monitor_fifo = None
    
    def build_phase(self):
        super().build_phase()
        
        self.vif = uart_if(name="vif", parent=self)
        self.vif.wire(self.dut)
        ConfigDB().set(context=self, inst_name="*", field_name="vif", value=self.vif)
        
        self.agent = uart_agent.create(name="agent", parent=self)
        self.monitor_fifo = uvm_tlm_analysis_fifo(name="monitor_fifo", parent=self)
        
    def connect_phase(self):
        super().connect_phase()

        self.agent.monitor.analysis_port.connect(self.monitor_fifo.analysis_export)
        
    async def receive_string(self, length: int) -> str:
        result = ""
        for _ in range(length):
            item: uart_sequence_item = await self.monitor_fifo.get()
            result += chr(item.byte)
        return result

    async def run_phase(self):
        self.raise_objection()
        await super().run_phase()

        self.logger.debug("waiting to receive 'hello uart'")
        received = await self.receive_string(10)
        self.logger.debug(f"received: '{received}'")
        assert received == "hello uart", f"expected 'hello uart', got '{received}'"

        self.vif.enable_transmit()
        await uart_string_sequence(string="hello back").start(self.agent.sequencer)
        self.vif.disable_transmit()
        self.logger.debug("transmitted: 'hello back'")

        # ignore garbage values if any recorded while transmitting to dut
        self.monitor_fifo.flush()
        first_item: uart_sequence_item = await self.monitor_fifo.get()
        first_char = chr(first_item.byte)
        
        if first_char == "r":
            rest = await self.receive_string(10)
            response = first_char + rest
        else:
            rest = await self.receive_string(9)
            response = first_char + rest
            
        self.logger.debug(f"response: '{response}'")
        assert response == "rodger that", f"dut reported error: '{response}'"

        self.logger.debug("run phase over, dropping objection")
        self.drop_objection()