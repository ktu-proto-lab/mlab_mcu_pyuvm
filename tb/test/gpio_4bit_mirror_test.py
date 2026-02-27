import pyuvm
from pyuvm import *
from env.gpio_env import gpio_env
from obj.gpio_seq_item import gpio_seq_item
from seq.gpio.gpio_4bit_rnd_seq import gpio_4bit_rnd_seq

@pyuvm.test()
class gpio_4bit_mirror_test(uvm_test):
    def build_phase(self):
        self.env = gpio_env(name="env", parent=self)

        self.fifo = uvm_tlm_analysis_fifo(name="fifo", parent=self)

    def connect_phase(self):
        self.env.agent.monitor.ap.connect(self.fifo.analysis_export)

    async def run_phase(self):
        self.raise_objection()

        seq = gpio_4bit_rnd_seq(name="gpio_4bit_rnd_seq")
        
        await seq.start(self.env.agent.seqr)

        self.drop_objection()