import cocotb
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
        self.tx_ap: uvm_analysis_port = None
        self.rx_ap: uvm_analysis_port = None

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

        self.tx_ap = uvm_analysis_port.create("tx_ap", self)
        self.rx_ap = uvm_analysis_port.create("rx_ap", self)

    async def bit_time(self, factor: float = 1.0):
        await Timer(self.vif.uart_bit_time_ns * factor, self.vif.clock_units, round_mode='round')


    async def monitor_tx(self):
        while True:
            await ReadOnly()

            # sync to idle
            if self.vif.uart_tx.value != 1:
                await RisingEdge(self.vif.uart_tx)
            # start bit
            await FallingEdge(self.vif.uart_tx)
            # middle of 0 bit frame
            await self.bit_time(factor=1.5)
            byte: UartByte = UartByte.create("rx_byte")
            for i in range(8):
                await ReadOnly()
                bit = self.vif.uart_tx.value.integer
                byte.val |= (bit << i)
                await self.bit_time()
            # clear stop bit frame
            await self.bit_time(factor=0.5)

            if not byte.is_idle_byte():
                self.logger.debug(f"uart tx: {byte}")
                self.tx_ap.write(byte)

    async def monitor_rx(self):
        while True:
            await ReadOnly()
            if self.vif.uart_rx.value != 1:
                await RisingEdge(self.vif.uart_rx)

            # start bit
            await FallingEdge(self.vif.uart_rx)
            # middle of 0 bit frame
            await self.bit_time(factor=1.5)
            byte = UartByte.create("rx_byte")
            for i in range(8):
                await ReadOnly()
                bit = self.vif.uart_rx.value.integer
                byte.val |= (bit << i)
                await self.bit_time()
            # clear stop bit frame
            await self.bit_time(factor=0.5)

            if not byte.is_idle_byte():
                self.logger.debug(f"uart rx: {byte}")
                self.rx_ap.write(byte)

    async def run_phase(self):
        await super().run_phase()

        # wait for system reset
        await RisingEdge(self.vif.reset)

        cocotb.start_soon(self.monitor_tx())
        cocotb.start_soon(self.monitor_rx())
