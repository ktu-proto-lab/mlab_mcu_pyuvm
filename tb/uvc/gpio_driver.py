from cocotb.triggers import RisingEdge, ReadWrite
from pyuvm import  ConfigDB, uvm_driver
from errors import ConfigError
from vif import McuVirtualInterface
from uvc.gpio_config import GpioConfig
from uvc.gpio_pad import GpioPad

class GpioDriver(uvm_driver):
    def __init__(self, name="GpioDriver", parent=None):
        super().__init__(name, parent)
        self.cfg: GpioConfig = None
        self.vif: McuVirtualInterface = None

    def build_phase(self):
        super().build_phase()

        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigError("no configuration provided for the gpio driver")

        self.cfg = ConfigDB().get(self, "", "cfg")

        self.vif = self.cfg.vif

    async def run_phase(self):
        await super().run_phase()

        await RisingEdge(self.vif.reset)

        while True:
            req: GpioPad = await self.seq_item_port.get_next_item()

            if not isinstance(req, GpioPad):
                raise TypeError(f"unknown sequence item provided, expeced GpioPins, got {type(req).__name__}")

            await ReadWrite()
            self.vif.top_gpio_o.value = req.state
            self.vif.top_gpio_oe.value = req.mask

            self.seq_item_port.item_done()
