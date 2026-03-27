import pyuvm
from pyuvm import ConfigDB, uvm_tlm_analysis_fifo
from test.base_test import base_test
from uvc.uart import uart_if, uart_agent, uart_sequence_item

@pyuvm.test()
class sw_io_printf_simple_test(base_test):
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
        
        expected: str = "printf: s: string, int: 189, int: -9021, uint: 1926478, int: 0, uint: 0, char: h, %r\x00"

        self.logger.debug(f"waiting to receive '{expected}'")
        received = await self.receive_string(len(expected))
        assert received == expected, f"expected {expected}, got '{received}'"
        self.logger.info(f"received: '{received}'")

        expected = "printf: over!\x00"
        received = await self.receive_string(len(expected))
        assert received == expected, f"expected {expected}, got '{received}'"
        self.logger.info(f"received: '{received}'")
        
        self.drop_objection()