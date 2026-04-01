import cocotb
from cocotb.handle import SimHandleBase
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge
from decimal import Decimal
from numbers import Real
from typing import cast

class mcu_vif:
    clock: SimHandleBase
    clock_units: str = 'ns'
    clock_period: Decimal = 12.5
    
    reset: SimHandleBase
    reset_duration: Decimal = 20
    
    exit_pad_io: SimHandleBase
    
    gpio_i: SimHandleBase
    gpio_o: SimHandleBase
    gpio_oe: SimHandleBase
    top_gpio_o: SimHandleBase
    top_gpio_oe: SimHandleBase
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
    
    def __init__(self, name = "mcu_vif", parent=None):
        
        self.clock = None
        self.reset = None
        
        self.exit_pad_io = None
        
        self.uart_tx = None
        self.uart_rx = None
        self.uart_rx_en = None
        
        self.gpio_i = None
        self.gpio_o = None
        self.gpio_oe = None
        self.top_gpio_o = None
        self.top_gpio_oe = None
        
        self.sda_i = None
        self.sda_o = None
        self.sda_oe = None
        
        self.scl_i = None
        self.scl_o = None
        self.scl_oe = None
    
    def wire(self, dut: SimHandleBase):
        self.clock = cast(SimHandleBase, dut.clk)
        self.reset = cast(SimHandleBase, dut.rst)
        
        self.exit_pad_io = cast(SimHandleBase, dut.ext_pad_io)
        
        self.uart_tx = cast(SimHandleBase, dut.ext_pad_io[1])
        self.uart_rx = cast(SimHandleBase, dut.top_gpio_o[0])
        self.uart_rx_en = cast(SimHandleBase, dut.top_gpio_oe[0])
        
        self.gpio_i = cast(SimHandleBase, dut.gpio_i)
        self.gpio_o = cast(SimHandleBase, dut.gpio_o)
        self.gpio_oe = cast(SimHandleBase, dut.gpio_oe)
        self.top_gpio_o = cast(SimHandleBase, dut.top_gpio_o)
        self.top_gpio_oe = cast(SimHandleBase, dut.top_gpio_oe)
        
        self.sda_i = cast(SimHandleBase, dut.sda_i)
        self.sda_o = cast(SimHandleBase, dut.sda_o)
        self.sda_oe = cast(SimHandleBase, dut.sda_oe_o)
        
        self.scl_i = cast(SimHandleBase, dut.scl_i)
        self.scl_o = cast(SimHandleBase, dut.scl_o)
        self.scl_oe = cast(SimHandleBase, dut.scl_oe_o)
    
    def release_clock(self):
        cocotb.start_soon(Clock(self.clock, self.clock_period, self.clock_units).start())
    
    async def reset_system(self):
        self.reset.value = 0
        await ClockCycles(self.clock, self.reset_duration)
        self.reset.value = 1
        
    async def reset_done(self):
        await RisingEdge(self.reset)
        
    async def clock_cycle(self):
        await ClockCycles(signal=self.clock, num_cycles=1, rising=True)
        
    async def clock_cycles(self, cycle_count: int):
        await ClockCycles(signal=self.clock, num_cycles=cycle_count, rising=True)
