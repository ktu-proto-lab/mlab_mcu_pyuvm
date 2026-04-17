from cocotb.triggers import ReadWrite, Timer
from pyuvm import uvm_driver, uvm_analysis_port, ConfigDB

from errors import ConfigTestError, VirtualInterfaceTestError

from vif.mcu_virtual_interface import McuVirtualInterface
from env.mcu_simulator import McuSimulatorEnum
from cfg.config import Config
from uvc.uart_byte import UartByte

class UartDriver(uvm_driver):
    def __init__(self, name="UartDriver", parent=None):
        super().__init__(name, parent)
        self.cfg: Config = None
        self.vif: McuVirtualInterface = None
        self.ap: uvm_analysis_port = None

    def build_phase(self):
        super().build_phase()

        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigTestError("no configuration provided for uart driver")

        self.cfg = ConfigDB().get(self, "", "cfg")

        if self.cfg.vif is None:
            raise VirtualInterfaceTestError("no provided virtual interface for uart driver")

        self.vif = self.cfg.vif

        if not isinstance(self.vif, McuVirtualInterface):
            raise TypeError(f"unknown virtual interface provided for uart driver: expected VirtualInterface, got {type(self.vif).__name__}")

        self.ap = uvm_analysis_port.create("ap", self)

    async def bit_time(self):
        await Timer(self.vif.uart_bit_time_ns, self.vif.clock_units, round_mode='round')

    async def run_phase(self):
        await super().run_phase()

        while True:
            byte: UartByte = await self.seq_item_port.get_next_item()

            if not isinstance(byte, UartByte):
                raise TypeError(f"uart driver only drives uart byte sequence items, expected UartByte, got {type(byte).__name__}")

            if self.cfg.simulator == McuSimulatorEnum.XCELIUM:
                # FIX (xcelium): 0.00s violation for read-write
                await Timer(1, units='ps')

            await ReadWrite()
            self.vif.uart_rx_en.value = 1
            self.vif.uart_rx.value = 1

            # wait for the monitor to sample the start bit to avoid false start detection
            await self.bit_time()

            # start bit
            self.vif.uart_rx.value = 0
            await self.bit_time()
            for i in range(8):
                bit = (byte.val >> i) & 1
                self.vif.uart_rx.value = bit
                await self.bit_time()
            # stop bit
            self.vif.uart_rx.value = 1
            await self.bit_time()

            await ReadWrite()
            self.vif.uart_rx_en.value = 0


            self.ap.write(byte)

            self.seq_item_port.item_done()
