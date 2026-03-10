from cocotb.handle import SimHandleBase
from cocotb.triggers import FallingEdge, RisingEdge, Timer
from vip.base_if import base_if

class uart_if(base_if):
    
    def __init__(self, dut: SimHandleBase, name="uart_if", parent=None):
        super().__init__(dut, name, parent)
        
        self.rx_pin_index = 1
        self.tx_pin_index = 0
        
        self.rx_i: SimHandleBase = dut.gpio_i[self.rx_pin_index]
        
        self.tx_o: SimHandleBase = dut.tb_gpio_o[self.tx_pin_index]
        self.tx_oe: SimHandleBase = dut.tb_gpio_oe[self.tx_pin_index]

        self.boud_rate = 115200
        self.bit_time = 1e9 / self.boud_rate
        
    def enable_transmit(self):
        self.tx_oe.value = 1
        # uart idle state is high
        self.tx_o.value = 1
        
    def disable_transmit(self):
        self.tx_oe.value = 0
    
    async def transmit_byte(self, byte: int):
        
        # start bit
        self.tx_o.value = 0
        await Timer(self.bit_time, units='ns')
        
        for i in range(8):
            bit = (byte >> i) & 1
            self.tx_o.value = bit
            
            await Timer(self.bit_time, units='ns')
            
        # stop bit
        self.tx_o.value = 1
        
        await Timer(self.bit_time, units='ns')
        
        
    async def receive_byte(self) -> int:
        
        if self.rx_i.value != 1:
            await RisingEdge(self.rx_i)
        
        # wait for start bit
        await FallingEdge(self.rx_i)
        
        # delay to sample the exactl middle value of a bit
        await Timer(self.bit_time * 1.5, units='ns', round_mode='round')
        
        byte: int = 0
        
        for i in range(8):
            bit = self.rx_i.value.integer
            byte |= (bit << i)
            
            await Timer(self.bit_time, units='ns', round_mode='round')
            
        # wait for stop bit (wait for remaining 0.5 bit time to clear the frame)
        await Timer(self.bit_time * 0.5, units='ns', round_mode='round')
        
        return byte
