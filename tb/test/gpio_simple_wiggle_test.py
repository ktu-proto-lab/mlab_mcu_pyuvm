import pyuvm
from test.mcu_base_test import McuBaseTest
from seq import GpioSequence

@pyuvm.test()
class GpioSimpleWiggleTest(McuBaseTest):
    def __init__(self, name="GpioWiggleTest", parent=None):
        super().__init__(name, parent)
        
    def build_phase(self):
        super().build_phase()
        self.env_cfg.uart.is_active = False
        self.logger.debug("build phase done")
        
    async def run_phase(self):
        self.raise_objection()
        self.logger.debug("raising the objection")
        await super().run_phase()
        cycle_count = 500
        self.logger.debug(f"waiting for {cycle_count} clock cycles for program to start it's state machine")
        await self.vif.clock_cycles(cycle_count)
        self.logger.debug(f"waiting for {cycle_count} done")
        gpio_sequence: GpioSequence = GpioSequence.create("gpio_sequence")
        self.logger.debug("created gpio sequence")
        self.logger.info("starting gpio sequence")
        # TODO (refac): move to the virtual sequencer
        await gpio_sequence.start(self.env.gpio_agent.sequencer)
        self.logger.info("gpio sequence completed")
        self.logger.debug("dropping the objection")
        self.drop_objection()
