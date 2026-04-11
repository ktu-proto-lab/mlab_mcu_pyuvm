from cocotb.triggers import RisingEdge, ReadOnly, FallingEdge, Timer
from pyuvm import uvm_monitor, uvm_analysis_port, ConfigDB

from errors import ConfigError, VirtualInterfaceError
from vif import VirtualInterface

from uvc.uart_byte import UartByte
from uvc.uart_config import UartConfig

class UartMonitor(uvm_monitor):
    def __init__(self, name="UartMonitor", parent=None):
        super().__init__(name, parent)
        self.cfg: UartConfig = None
        self.vif: VirtualInterface = None
        self.ap: uvm_analysis_port = None
        
    def build_phase(self):
        super().build_phase()

        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigError("no configuration provided for uart monitor")
        
        self.cfg = ConfigDB().get(self, "", "cfg")
        
        if self.cfg.vif is None:
            raise VirtualInterfaceError("no provided virtual interface for uart driver")
        
        self.vif = self.cfg.vif
        
        if not isinstance(self.vif, VirtualInterface):
            raise TypeError(f"unknown virtual interface provided for uart monitor: expected VirtualInterface, got {type(self.vif).__name__}")
        
        self.ap = uvm_analysis_port.create("ap", self)
        
    
    async def run_phase(self):
        await super().run_phase()
        
        async def bit_time(factor: float = 1.0):
            await Timer(self.vif.uart_bit_time_ns * factor, self.vif.clock_units, round_mode='round')

        await RisingEdge(self.vif.reset)
        
        while True:
            await ReadOnly()
            
            self.logger.debug("receiving byte")
            # sync to idle
            if self.vif.uart_tx.value != 1:
                await RisingEdge(self.vif.uart_tx)
            # start bit
            await FallingEdge(self.vif.uart_tx)
            # middle of 0 bit frame
            await bit_time(factor=1.5)
            byte: UartByte = UartByte.create("rx_byte")
            for i in range(8):
                bit = self.vif.uart_tx.value.integer
                byte.val |= (bit << i)
                await bit_time()
            # clear stop bit frame
            await bit_time(factor=0.5)
            
            if byte.is_idle_byte():
                continue
            
            self.logger.debug(f"received {byte}")
            self.ap.write(byte)
