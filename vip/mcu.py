import cocotb
from cocotb.handle import SimHandleBase
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge
from decimal import Decimal
from pyuvm import uvm_component
from numbers import Real
from typing import cast

class mcu(uvm_component):
    dut: SimHandleBase
    
    clock: SimHandleBase
    clock_units: str = 'ns'
    clock_period: Decimal = 12.5
    
    reset: SimHandleBase
    reset_duration: Decimal = 20
    
    gpio_i: SimHandleBase
    gpio_o: SimHandleBase
    gpio_oe: SimHandleBase
    gpio_count: Decimal = 10
    
    uart_tx: SimHandleBase
    uart_rx: SimHandleBase
    uart_rx_en: SimHandleBase
    uart_boud_rate: Decimal = 115200
    
    def __init__(self, name, parent):
        super().__init__(name, parent)
        
        self.dut = cocotb.top
        
    def build_phase(self):
        super().build_phase()

        self.clock = self.dut.clk
        self.reset = self.dut.rst
        
        self.uart_tx = self.dut.ext_pad_io[1]
        self.uart_rx = self.dut.tb_gpio_o[0]
        self.uart_rx_en = self.dut.tb_gpio_oe[0]
        
        self.gpio_i = self.dut.gpio_i
        self.gpio_o = self.dut.tb_gpio_o
        self.gpio_oe = self.dut.tb_gpio_oe
        
    async def run_phase(self):
        await super().run_phase()
        
        cocotb.start_soon(Clock(self.clock, self.clock_period, self.clock_units).start())
        self.logger.debug(f"system clock started with period of {self.clock_period}{self.clock_units}")
        
        self.reset.value = 0
        self.logger.debug(f"system wide reset for {self.reset_duration} clock cycles")
        await ClockCycles(self.clock, self.reset_duration)
        self.reset.value = 1
        self.logger.debug("system wide reset done")
    
    async def reset_done(self):
        await RisingEdge(self.reset)
        
    async def clock_cycle(self):
        await ClockCycles(signal=self.clock, num_cycles=1, rising=True)
        
    async def clock_cycles(self, cycle_count: int):
        await ClockCycles(signal=self.clock, num_cycles=cycle_count, rising=True)
