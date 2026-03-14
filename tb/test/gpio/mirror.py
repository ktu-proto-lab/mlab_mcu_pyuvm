import pyuvm
from cocotb.triggers import ClockCycles
from tb.test.gpio.base import gpio_base_test
from vip.gpio.gpio_sequence import gpio_4bit_random_sequence

@pyuvm.test()
class gpio_mirror_test(gpio_base_test):
    def build_phase(self):
        super().build_phase()

    async def run_phase(self):
        self.raise_objection()
        
        await super().run_phase()
        
        # wait for main function to initialize gpio regs
        await ClockCycles(self.dut.clk, 500)

        sequence: gpio_4bit_random_sequence = gpio_4bit_random_sequence.create(name="gpio_4bit_random_sequence")
        
        await sequence.start(self.env.agent.sequencer)
        
        await ClockCycles(self.dut.clk, 1000)
        
        self.drop_objection()
        
    def report_phase(self):
        super().report_phase()
        
        assert self.env.scoreboard.failure == 0, (
            f"Test failed with {self.env.scoreboard.failure} scoreboard errors"
        )
