import pyuvm
import cocotb
from pyuvm import *
from pyuvm import ConfigDB
from tb.test.base import base_test
from vip.uart.agent import uart_agent
from vip.uart.vif import uart_if
from vip.uart.sequence import uart_string_sequence

@pyuvm.test()
class uart_greet_test(base_test):
    def build_phase(self):
        super().build_phase()
        
        self.vif = uart_if(dut=self.dut, name="vif", parent=self)

        ConfigDB().set(context=self, inst_name="*", field_name="vif", value=self.vif)
        
        self.agent = uart_agent(name="agent", parent=self)
        
    async def run_phase(self):
        self.raise_objection()
        await super().run_phase()

        self.vif.enable_receive()
        self.logger.debug("waiting to receive 'hello uart'")
        
        await self.vif.system_clock_cycles(90_000)
        self.vif.disable_receive()

        self.vif.enable_transmit()
        transmit_sequence = uart_string_sequence(string="hello back")
        self.logger.debug(f"transmitting: {transmit_sequence}")
        await transmit_sequence.start(self.agent.sequencer)
        self.logger.debug(f"transmitted: {transmit_sequence}")
        self.vif.disable_transmit()

        self.vif.enable_receive()
        await self.vif.system_clock_cycles(100_000)
        self.vif.disable_receive()

        self.logger.debug("run phase over, dropping objection")
        self.drop_objection()