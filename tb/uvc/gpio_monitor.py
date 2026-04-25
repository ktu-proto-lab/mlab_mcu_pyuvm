from cocotb.triggers import RisingEdge, ReadOnly
from pyuvm import uvm_monitor, uvm_analysis_port, ConfigDB
from errors import ConfigTestError

from env.mcu_simulator import McuSimulatorEnum
from uvc.gpio_config import GpioConfig
from uvc.gpio_pad import GpioPad

class GpioMonitor(uvm_monitor):
    def __init__(self, name="GpioMonitor", parent=None):
        super().__init__(name, parent)
        self.cfg: GpioConfig = None
        self.ap: uvm_analysis_port = None

    def build_phase(self):
        super().build_phase()

        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigTestError("no provided configuration for gpio monitor")

        self.cfg = ConfigDB().get(self, "", "cfg")
        
        if not isinstance(self.cfg, GpioConfig):
            raise ConfigTestError(
                f"invalid configuration type for gpio monitor, expected GpioConfig, got {type(self.cfg).__name__}"
            )

        self.vif = self.cfg.vif

        self.ap = uvm_analysis_port.create("ap", self)

    async def run_phase(self):
        await super().run_phase()

        await RisingEdge(self.vif.reset)

        prev_pin_state: int = None

        while True:
            await RisingEdge(self.vif.clock)
            await ReadOnly()

            if self.cfg.simulator == McuSimulatorEnum.XCELIUM:
                # FIX (XCELIUM): x and z states
                if not self.vif.exit_pad_io.value.is_resolvable:
                    continue

            curr_pin_state: int = self.vif.exit_pad_io.value

            if curr_pin_state != prev_pin_state:
                txn: GpioPad = GpioPad.create("txn")
                txn.state = curr_pin_state
                self.logger.debug(f"{txn}")
                self.ap.write(txn)
                prev_pin_state = curr_pin_state
