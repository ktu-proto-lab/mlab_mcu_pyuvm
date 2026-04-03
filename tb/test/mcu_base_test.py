import pyuvm
from pyuvm import ConfigDB
from test.base_test import BaseTest
from env import McuEnv
from uvc.gpio import GpioAgent, GpioInterface, GpioDriver
from uvc.uart import UartInterface
from vif import McuVirtualInterface

@pyuvm.test()
class McuBaseTest(BaseTest):
    def __init__(self, name="McuBaseTest", parent=None):
        super().__init__(name, parent)
        self.vif: McuVirtualInterface = None
        self.gpio_if: GpioInterface = None
        self.uart_if: UartInterface = None
        self.env_cfg: McuEnv.Config = None
        self.env: McuEnv = None

    def build_phase(self):
        super().build_phase()
        self.vif = McuVirtualInterface("vif", self)
        self.vif.wire(self.dut)
        self.logger.info("mcu virtual interface wired to the dut")
        self.gpio_if = GpioInterface("gpio_if", self)
        self.gpio_if.map(self.vif)
        self.logger.info("gpio interface mapped to mcu virtual interface")
        self.uart_if = UartInterface("uart_if", self)
        self.uart_if.map(self.vif)
        self.logger.info("uart interface mapped to mcu virtual interface")
        self.env_cfg = McuEnv.Config.create("env_cfg")
        self.logger.debug("built mcu environment configuration")
        self.env_cfg.gpio.vif = self.gpio_if
        self.logger.debug("assigned gpio interface to the mcu environment configuration")
        self.env_cfg.uart.vif = self.uart_if
        self.logger.debug("assigned uart interface to the mcu environment configuration")
        ConfigDB().set(self, "env", "cfg", self.env_cfg)
        self.env = McuEnv.create("env", self)
        self.logger.info("mcu environment created")
        self.logger.debug("build phase done")

    async def run_phase(self):
        self.raise_objection()
        self.logger.debug("raising the objection")
        await super().run_phase()
        self.logger.debug("releasing system clock")
        # TODO (feat): save clock task so on simulation end it is terminated safelly
        self.vif.release_clock()
        self.logger.info(f"system clock: {self.vif.clock_period}{self.vif.clock_units}")
        self.logger.info(f"system reset for {self.vif.reset_duration} clock cycles")
        await self.vif.read_only()
        assert self.vif.reset.value == 0, "expected reset low"
        await self.vif.reset_system()
        await self.vif.read_only()
        assert self.vif.reset.value == 1, "expected reset high"
        self.logger.debug("system reset: done")
        self.logger.debug("dropping the objection")
        self.drop_objection()
