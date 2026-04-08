from pyuvm import ConfigDB, uvm_monitor, uvm_object, uvm_analysis_port
from cocotb.triggers import ReadOnly, RisingEdge
from error import ConfigError
from uvc.gpio.gpio_transaction import GpioTransaction
from uvc.gpio.gpio_interface import GpioInterface

class GpioMonitor(uvm_monitor):
    class Config(uvm_object):
        def __init__(self, name="GpioMonitorConfig"):
            super().__init__(name)
            self.vif: GpioInterface = None
            self.is_active: bool = True
            self.mask: int = 0xFF

    def __init__(self, name="GpioMonitor", parent=None):
        super().__init__(name, parent)
        self.cfg: GpioMonitor.Config = None
        self.analysis_port: uvm_analysis_port = None

    def build_phase(self):
        super().build_phase()
        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigError("no configuration provided for the gpio monitor", self)
        self.cfg = ConfigDB().get(self, "", "cfg")
        if self.cfg.vif is None:
            raise ConfigError("no provided interface for the gpio monitor")
        self.logger.info(f"gpio monitor configuration: active={self.cfg.is_active}, mask={self.cfg.mask}")
        self.analysis_port = uvm_analysis_port(name="analysis_port", parent=self)

    async def run_phase(self):
        await super().run_phase()
        if not self.cfg.is_active:
            self.logger.info("gpio monitor is not active")
            return
        await self.cfg.vif.system_reset_done()
        prev_value: int = None
        while True:
            await RisingEdge(self.cfg.vif.system_clock)
            await ReadOnly()
            curr_value: int = self.cfg.vif.read_pins(self.cfg.mask)
            if curr_value is None:
                continue
            if curr_value != prev_value:
                txn = GpioTransaction("gpio_mon_tr", curr_value)
                self.logger.debug(f"{txn}")
                self.analysis_port.write(txn)
                prev_value = curr_value
