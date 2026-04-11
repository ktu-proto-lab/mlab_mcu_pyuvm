from cocotb.triggers import ReadWrite, Timer
from pyuvm import uvm_driver, uvm_analysis_port, ConfigDB

from errors import ConfigError, VirtualInterfaceError
from vif import VirtualInterface

from uvc.uart_config import UartConfig
from uvc.uart_byte import UartByte

class UartDriver(uvm_driver):
    def __init__(self, name="UartDriver", parent=None):
        super().__init__(name, parent)
        self.cfg: UartConfig = None
        self.vif: VirtualInterface = None
        self.ap: uvm_analysis_port = None
        
    def build_phase(self):
        super().build_phase()

        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigError("no configuration provided for uart driver")
        
        self.cfg = ConfigDB().get(self, "", "cfg")
        
        if self.cfg.vif is None:
            raise VirtualInterfaceError("no provided virtual interface for uart driver")
        
        self.vif = self.cfg.vif
        
        if not isinstance(self.vif, VirtualInterface):
            raise TypeError(f"unknown virtual interface provided for uart driver: expected VirtualInterface, got {type(self.vif).__name__}")
        
        self.ap = uvm_analysis_port.create("ap", self)
        
    async def run_phase(self):
        super().run_phase()
        
        async def bit_time():
            await Timer(self.vif.uart_bit_time_ns, self.vif.clock_units, 'round')

        while True:
            byte: UartByte = await self.seq_item_port.get_next_item()

            if not isinstance(byte, UartByte):
                raise TypeError(f"uart driver only drives uart byte sequence items, expected UartByte, got {type(byte).__name__}")
            
            self.logger.debug(f"transmitting byte '{byte}'")
            await ReadWrite()
             # start bit
            self.transmit.value = 0
            await bit_time()
            for i in range(8):
                bit = (byte >> i) & 1
                self.transmit.value = bit
                await bit_time()
            # stop bit
            self.transmit.value = 1
            await bit_time()
            self.logger.debug(f"transmitted '{byte}'")

            self.ap.write(byte)
            
            self.seq_item_port.item_done()
