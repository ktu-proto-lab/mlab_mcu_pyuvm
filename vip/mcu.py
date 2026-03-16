import cocotb
from cocotb.handle import SimHandleBase
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge
from decimal import Decimal
from numbers import Real
from pyuvm import uvm_component
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
    uart_bit_time_ns: Real = 1e9 / uart_boud_rate
    
    sda_i: SimHandleBase
    sda_o: SimHandleBase
    sda_oe: SimHandleBase
    
    scl_i: SimHandleBase
    scl_o: SimHandleBase
    scl_oe: SimHandleBase
    
    def build_phase(self):
        super().build_phase()
        
        self.dut = cocotb.top
        
        self.logger.debug("build phase done")

    def connect_phase(self):
        super().connect_phase()

        self.clock = cast(SimHandleBase, self.dut.clk)
        self.reset = cast(SimHandleBase, self.dut.rst)
        
        self.uart_tx = cast(SimHandleBase, self.dut.ext_pad_io[1])
        self.uart_rx = cast(SimHandleBase, self.dut.tb_gpio_o[0])
        self.uart_rx_en = cast(SimHandleBase, self.dut.tb_gpio_oe[0])
        
        self.gpio_i = cast(SimHandleBase, self.dut.gpio_i)
        self.gpio_o = cast(SimHandleBase, self.dut.tb_gpio_o)
        self.gpio_oe = cast(SimHandleBase, self.dut.tb_gpio_oe)
        
        self.sda_i = cast(SimHandleBase, self.dut.sda_pad_i)
        self.sda_o = cast(SimHandleBase, self.dut.sda_pad_o)
        self.sda_oe = cast(SimHandleBase, self.dut.sda_padoen_o)
        
        self.scl_i = cast(SimHandleBase, self.dut.scl_pad_i)
        self.scl_i = cast(SimHandleBase, self.dut.scl_pad_o)
        self.scl_i = cast(SimHandleBase, self.dut.scl_padoen_o)
        
        self.logger.debug("connect phase done")
        
    async def run_phase(self):
        await super().run_phase()
        
        cocotb.start_soon(Clock(self.clock, self.clock_period, self.clock_units).start())
        self.logger.debug(f"system clock started with period of {self.clock_period}{self.clock_units}")
        
        self.reset.value = 0
        self.logger.debug(f"system wide reset for {self.reset_duration} clock cycles")
        await ClockCycles(self.clock, self.reset_duration)
        self.reset.value = 1
        self.logger.debug("system wide reset done")
        
        self.logger.debug("run phase done")
    
    async def reset_done(self):
        await RisingEdge(self.reset)
        
    async def clock_cycle(self):
        await ClockCycles(signal=self.clock, num_cycles=1, rising=True)
        
    async def clock_cycles(self, cycle_count: int):
        await ClockCycles(signal=self.clock, num_cycles=cycle_count, rising=True)
