from cocotb.handle import SimHandleBase
from cocotb.triggers import FallingEdge, RisingEdge, Timer, Event, ReadOnly
from decimal import Decimal
from numbers import Real
from typing import cast
from vip.base_vif import base_vif

class uart_vif(base_vif):
    
    transmit: SimHandleBase
    transmit_pin: int = 0
    transmit_enable: SimHandleBase
    
    receive: SimHandleBase
    receive_pin: int = 1
    
    boud_rate: Decimal = 115200
    bit_time_ns: Real = 1e9 / boud_rate
    
    def __init__(self, dut: SimHandleBase, name="uart_if", parent=None):
        super().__init__(dut, name, parent)
        
        self.transmit = cast(SimHandleBase, dut.tb_gpio_o[self.transmit_pin])
        self.transmit_enable= cast(SimHandleBase, dut.tb_gpio_oe[self.transmit_pin])
        
        self.receive = cast(SimHandleBase, dut.ext_pad_io[self.receive_pin])

        self.boud_rate: Decimal = 115200
        self.bit_time_ns: Real = 1e9 / self.boud_rate
        
    def enable_transmit(self):
        self.transmit_enable.value = 1
        self.transmit.value = 1
        
    def disable_transmit(self):
        self.transmit_enable.value = 0
        
    async def bit_time(self, factor: float = 1.0):
        await Timer(self.bit_time_ns * factor, units='ns', round_mode='round')
    
    async def transmit_byte(self, byte: int):
        # start bit
        self.transmit.value = 0
        await self.bit_time()
        
        for i in range(8):
            bit = (byte >> i) & 1
            self.transmit.value = bit
            await self.bit_time()
            
        # stop bit
        self.transmit.value = 1
        await self.bit_time()     
        
    async def receive_byte(self) -> int:
        # sync to idle
        await ReadOnly()
        if self.receive.value != 1:
            await RisingEdge(self.receive)

        # start bit
        await FallingEdge(self.receive)
        
        # middle of 0 bit frame
        await self.bit_time(factor=1.5)

        byte: int = 0
        for i in range(8):
            bit = self.receive.value.integer
            byte |= (bit << i)
            await self.bit_time()
            
        # clear stop bit frame
        await self.bit_time(factor=0.5)
        
        return byte
