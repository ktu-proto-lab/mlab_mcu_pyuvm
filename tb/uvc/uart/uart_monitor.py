from cocotb.triggers import RisingEdge, ReadOnly
from pyuvm import uvm_monitor, uvm_analysis_port, ConfigDB, uvm_object
from typing import cast
from uvc.uart.uart_interface import UartInterface
from uvc.uart.uart_transaction import UartTransaction
from log.error import ConfigError

class UartMonitor(uvm_monitor):
    class Config(uvm_object):
        def __init__(self, name="UartMonitorConfig"):
            super().__init__(name)
            self.vif: UartInterface = None
            self.is_active: bool = True

    def __init__(self, name="UartMonitor", parent=None):
        super().__init__(name, parent)
        self.cfg: UartMonitor.Config = None
        self.analysis_port: uvm_analysis_port = None
    
    def build_phase(self):
        super().build_phase()
        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigError("no configuration provided for the uart monitor", self)
        self.cfg = ConfigDB().get(self, "", "cfg")
        if self.cfg.vif is None:
            raise ConfigError("no provided interface for the uart monitor")
        # TODO (refac): better use __str__() in configuration class
        self.logger.info(f"uart monitor configuration: active={self.cfg.is_active}")
        self.analysis_port = uvm_analysis_port("analysis_port", self)

    async def run_phase(self):
        await super().run_phase()
        if not self.cfg.is_active:
            self.logger.info("uart monitor is not active")
            return
        await self.cfg.vif.system_reset_done()
        while True:
            byte: int = await self.cfg.vif.receive_byte()
            txn = UartTransaction("txn", byte)
            self.logger.debug(f"{txn}")
            self.analysis_port.write(txn)
