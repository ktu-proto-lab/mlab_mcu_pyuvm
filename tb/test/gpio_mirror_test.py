import pyuvm
from pyuvm import *
from cocotb.triggers import Timer
from env.gpio_env import gpio_env
from obj.gpio_seq_item import gpio_seq_item
from seq.gpio.gpio_4bit_rnd_seq import gpio_4bit_rnd_seq

@pyuvm.test()
class gpio_mirror_test(uvm_test):
    def build_phase(self):
        super().build_phase()
        
        self.env = gpio_env(name="env", parent=self)

        self.fifo = uvm_tlm_analysis_fifo(name="fifo", parent=self)

    def connect_phase(self):
        self.env.agent.monitor.ap.connect(self.fifo.analysis_export)

    async def run_phase(self):
        await super().run_phase()
        
        self.raise_objection()

        seq = gpio_4bit_rnd_seq(name="gpio_4bit_rnd_seq")
        
        await seq.start(self.env.agent.seqr)
        
        await Timer(5_000, 'ns')

        self.drop_objection()
        
    def report_phase(self):
        super().report_phase()
        
        assert self.env.scoreboard.failure == 0, (
            f"Test failed with {self.env.scoreboard.failure} scoreboard errors"
        )