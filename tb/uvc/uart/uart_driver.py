from pyuvm import uvm_driver, ConfigDB, uvm_analysis_port, uvm_object
from uvc.uart.uart_interface import UartInterface
from uvc.uart.uart_transaction import UartTransaction
from log.error import ConfigError

class UartDriver(uvm_driver):
    class Config(uvm_object):
        def __init__(self, name="UartDriverConfig"):
            super().__init__(name)
            self.vif: UartInterface = None
            self.is_active: bool = True

    def __init__(self, name="GpioDriver", parent=None):
        super().__init__(name, parent)
        self.cfg: UartDriver.Config = None
        self.analysis_port = None

    def build_phase(self):
        super().build_phase()
        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigError("no configuration provided for the uart driver")
        self.cfg = ConfigDB().get(self, "", "cfg")
        if not self.cfg.is_active:
            self.logger.debug("uart driver is not active")
            return
        if self.cfg.vif is None:
            raise ConfigError("no provided interface for the uart driver")
        self.logger.info(f"uart driver configuration: active={self.cfg.is_active}")
        self.analysis_port = uvm_analysis_port(name="analysis_port", parent=self)

    async def run_phase(self):
        await super().run_phase()
        if not self.cfg.is_active:
            self.logger.info("uart driver is not active")
            return
        while True:
            txn: UartTransaction = await self.seq_item_port.get_next_item()
            self.logger.debug(f"{txn.hex_value()}")
            await self.cfg.vif.transmit_byte(txn.byte)
            self.analysis_port.write(txn)
            self.seq_item_port.item_done()
