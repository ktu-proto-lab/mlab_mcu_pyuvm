from pyuvm import  ConfigDB, uvm_analysis_port, uvm_driver, uvm_object
from log.error import ConfigError
from uvc.gpio.gpio_interface import GpioInterface
from uvc.gpio.gpio_transaction import GpioTransaction

class GpioDriver(uvm_driver):
    class Config(uvm_object):
        def __init__(self, name="GpioDriverConfig"):
            super().__init__(name)
            self.vif: GpioInterface = None
            self.is_active: bool = True
            self.mask: int = 0xFF

    def __init__(self, name="GpioDriver", parent=None):
        super().__init__(name, parent)
        self.cfg: GpioDriver.Config = None
        self.analysis_port: uvm_analysis_port = None

    def build_phase(self):
        super().build_phase()
        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigError("no configuration provided for the gpio driver")
        self.cfg = ConfigDB().get(self, "", "cfg")
        if self.cfg.vif is None:
            raise ConfigError("no provided interface for the gpio driver")
        self.logger.info(f"gpio driver configuration: active={self.cfg.is_active}, mask={self.cfg.mask}")
        self.analysis_port = uvm_analysis_port("analysis_port", self)

    async def run_phase(self):
        await super().run_phase()
        if not self.cfg.is_active:
            self.logger.info("gpio driver is not active")
            return
        while True:
            txn: GpioTransaction = await self.seq_item_port.get_next_item()
            self.cfg.vif.drive_input(txn.value, self.cfg.mask)
            self.logger.debug(f"{hex(txn.value)}")
            self.analysis_port.write(txn)
            await self.cfg.vif.system_clock_cycles(1000)
            self.seq_item_port.item_done()
