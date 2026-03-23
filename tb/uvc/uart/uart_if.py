from cocotb.handle import SimHandleBase
from cocotb.triggers import FallingEdge, RisingEdge, Timer, ReadOnly
from decimal import Decimal
from numbers import Real
from uvc.base_if import base_if
from vif import mcu_vif

class uart_if(base_if):
    
    transmit: SimHandleBase
    transmit_enable: SimHandleBase
    receive: SimHandleBase
    
    boud_rate: Decimal
    bit_time_ns: Real
    
    def __init__(self, name="uart_if", parent=None):
        super().__init__(name, parent)
        
        self.transmit = None
        self.transmit_enable = None
        self.receive = None
        
        self.boud_rate = None
        self.bit_time_ns = None

    def wire(self, dut: mcu_vif):
        super().wire(dut)
        
        self.transmit = dut.uart_rx
        self.transmit_enable = dut.uart_rx_en
        self.receive = dut.uart_tx
        
        self.boud_rate = dut.uart_boud_rate
        self.bit_time_ns = dut.uart_bit_time_ns

        
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
