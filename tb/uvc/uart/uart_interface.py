from cocotb.handle import SimHandleBase
from cocotb.triggers import FallingEdge, RisingEdge, Timer, ReadOnly
from decimal import Decimal
from numbers import Real
from uvc.system_interface import SystemInterface
from vif import McuVirtualInterface

class UartInterface(SystemInterface):
    def __init__(self, name="UartInterface", parent=None):
        super().__init__(name, parent)
        self.transmit: SimHandleBase = None
        self.transmit_enable: SimHandleBase = None
        self.receive: SimHandleBase = None
        self.boud_rate: Decimal = None
        self.bit_time_ns: Real = None

    def map(self, vif: McuVirtualInterface):
        super().map(vif)
        self.transmit = vif.uart_rx
        self.transmit_enable = vif.uart_rx_en
        self.receive = vif.uart_tx
        self.boud_rate = vif.uart_boud_rate
        self.bit_time_ns = vif.uart_bit_time_ns
        
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
