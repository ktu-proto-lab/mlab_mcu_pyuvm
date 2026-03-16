import cocotb
import pyuvm
from tb.test.base import base_test
from vip.uart.sequence_item import uart_sequence_item
from vip.uart.sequence import uart_string_sequence
from vip.uart.vif import uart_vif
from vip.uart.agent import uart_agent
from pyuvm import ConfigDB, uvm_tlm_analysis_fifo
from vip.mcu import mcu

@pyuvm.test()
class uart_greet_test(base_test):
    def build_phase(self):
        super().build_phase()
        self.mcu: mcu = mcu.create(name="mcu", parent=self)
        self.vif = uart_vif(dut=cocotb.top, name="vif", parent=self)
        ConfigDB().set(self, "*", "vif", self.vif)
        self.agent = uart_agent("agent", self)
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
        await self.mcu.run_phase()

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