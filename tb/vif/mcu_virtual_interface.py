import cocotb
from cocotb.handle import SimHandleBase
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, ReadOnly
from decimal import Decimal
from numbers import Real
from typing import cast

class McuVirtualInterface:
    def __init__(self, name="McuVirtualInterface", parent=None):
        # TODO (feat): add logger and print name and the parent
        self.clock: SimHandleBase = None
        self.clock_units: str = 'ns'
        self.clock_period: Decimal = 12.5
        self.reset: SimHandleBase = None
        self.reset_duration: Decimal = 20
        self.exit_pad_io: SimHandleBase = None
        self.gpio_i: SimHandleBase = None
        self.gpio_o: SimHandleBase = None
        self.gpio_oe: SimHandleBase = None
        # TODO (refac): rename to gpio_top_o and gpio_top_oe
        self.top_gpio_o: SimHandleBase = None
        self.top_gpio_oe: SimHandleBase = None
        self.gpio_count: Decimal = 10
        self.uart_tx: SimHandleBase = None
        self.uart_rx: SimHandleBase = None
        self.uart_rx_en: SimHandleBase = None
        self.uart_boud_rate: Decimal = 115200
        self.uart_bit_time_ns: Real = 1e9 / self.uart_boud_rate
        self.sda_i: SimHandleBase = None
        self.sda_o: SimHandleBase = None
        self.sda_oe: SimHandleBase = None
        self.scl_i: SimHandleBase = None
        self.scl_o: SimHandleBase = None
        self.scl_oe: SimHandleBase = None
    
    def wire(self, dut: SimHandleBase):
        # TODO (feat): check if dut contains expected signals
        self.clock = cast(SimHandleBase, dut.clk)
        self.reset = cast(SimHandleBase, dut.rst)
        self.exit_pad_io = cast(SimHandleBase, dut.ext_pad_io)
        self.gpio_i = cast(SimHandleBase, dut.gpio_i)
        self.gpio_o = cast(SimHandleBase, dut.gpio_o)
        self.gpio_oe = cast(SimHandleBase, dut.gpio_oe)
        self.top_gpio_o = cast(SimHandleBase, dut.top_gpio_o)
        self.top_gpio_oe = cast(SimHandleBase, dut.top_gpio_oe)
        # TODO (refac): add constants on which exit pads uart pins are wired to
        self.uart_tx = cast(SimHandleBase, dut.ext_pad_io[1])
        self.uart_rx = cast(SimHandleBase, dut.top_gpio_o[0])
        self.uart_rx_en = cast(SimHandleBase, dut.top_gpio_oe[0])
        self.sda_i = cast(SimHandleBase, dut.sda_i)
        self.sda_o = cast(SimHandleBase, dut.sda_o)
        self.sda_oe = cast(SimHandleBase, dut.sda_oe_o)
        self.scl_i = cast(SimHandleBase, dut.scl_i)
        self.scl_o = cast(SimHandleBase, dut.scl_o)
        self.scl_oe = cast(SimHandleBase, dut.scl_oe_o)
    
    def release_clock(self):
        cocotb.start_soon(Clock(self.clock, self.clock_period, self.clock_units).start())
    
    async def reset_system(self):
        await RisingEdge(self.clock)
        self.reset.value = 0
        await ClockCycles(self.clock, self.reset_duration)
        self.reset.value = 1
        
    async def reset_done(self):
        await RisingEdge(self.reset)
        
    async def clock_cycle(self):
        await ClockCycles(signal=self.clock, num_cycles=1, rising=True)
        
    async def clock_cycles(self, cycle_count: int):
        await ClockCycles(signal=self.clock, num_cycles=cycle_count, rising=True)
        
    async def read_only(self):
        await ReadOnly()
