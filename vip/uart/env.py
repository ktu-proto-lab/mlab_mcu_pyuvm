import cocotb
from cocotb.handle import SimHandleBase
from pyuvm import uvm_env
from vip.uart.agent import uart_agent
from vip.uart.vif import uart_vif
from vip.uart.scoreboard import uart_scoreboard

class uart_env(uvm_env):

    dut: SimHandleBase
    vif: uart_vif
    agent: uart_agent
    scoreboard: uart_scoreboard
    
    def build_phase(self):
        super().build_phase()

        self.dut = cocotb.top
        self.vif = uart_vif(dut=self.dut, name="vif", parent=self)
        self.agent = uart_agent.create(name="agent", parent=self)
        self.scoreboard = uart_scoreboard.create(name="scoreboard", parent=self)
        
    def connect_phase(self):
        super().connect_phase()

        self.agent.driver.analysis_port.connect(self.scoreboard.transmit_fifo.analysis_export)
        self.agent.monitor.analysis_port.connect(self.scoreboard.receive_fifo.analysis_export)
        