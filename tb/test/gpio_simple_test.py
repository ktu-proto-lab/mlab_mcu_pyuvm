import pyuvm
from cocotb.triggers import ClockCycles
from test import base_test
from seq import gpio_sequence
from env.gpio import gpio_env

@pyuvm.test()
class gpio_simple_test(base_test):
    def build_phase(self):
        super().build_phase()
        
        self.env = gpio_env.create("env", self)

    async def run_phase(self):
        self.raise_objection()
        
        await super().run_phase()
        
        # wait for main function to initialize gpio regs
        await ClockCycles(self.dut_vif.clock, 500)

        sequence = gpio_sequence.create(name="gpio_sequence")
        
        await sequence.start(self.env.input_agent.sequencer)
        
        await ClockCycles(self.dut_vif.clock, 1000)
        
        self.drop_objection()
        
    def report_phase(self):
        super().report_phase()
        
        assert self.env.scoreboard.failure == 0, (
            f"Test failed with {self.env.scoreboard.failure} scoreboard errors"
        )
