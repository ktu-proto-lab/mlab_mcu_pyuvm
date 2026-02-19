import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, ReadOnly
from pyuvm import *
from vif.gpio import gpio

class gpio_env(uvm_env):

    def build_phase(self):
        self.dut = cocotb.top
        self.vif = gpio(self.dut)

    async def run_phase(self):
        self.raise_objection()

        cocotb.start_soon(Clock(self.dut.clk, 10, units="ns").start())

        self.dut.rst.value = 0
        await ClockCycles(self.dut.clk, 10)
        self.dut.rst.value = 1

        self.dut._log.info("Waiting for GPIO_PIN_0 output")

        CLOCK_CYCLES = 100_000
        for i in range(200):

            await ClockCycles(self.dut.clk, CLOCK_CYCLES)
            await ReadOnly()

            if self.dut.ext_pad_io[0].value.integer == 1:
                self.dut._log.info(f"GPIO_PIN_0 = {self.vif.read_pin(0)}, GPIO pin values: {self.vif.read_pins_binsrt()}")
                assert self.vif.read_pin(0) == 1, f"GPIO values: {self.vif.read_pins_binsrt()}"
                break
            
            self.dut._log.info(f"After {i * CLOCK_CYCLES} I/O pad value: {self.vif.read_pins_binsrt()}")

        self.drop_objection()