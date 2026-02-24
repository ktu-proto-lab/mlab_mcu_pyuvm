from pyuvm import *
from cocotb.triggers import ClockCycles, ReadOnly, RisingEdge
from cocotb.handle import SimHandleBase
from vif.gpio import gpio
from obj.gpio_seq_item import gpio_seq_item


class gpio_monitor(uvm_monitor):
    def build_phase(self):
        super().build_phase()

        self.dut: SimHandleBase = ConfigDB().get(context=self, inst_name="", field_name="dut")

        self.vif: gpio = ConfigDB().get(context=self, inst_name="", field_name="vif")

        # Broadcast to the Scoreboard
        self.ap = uvm_analysis_port(name="ap", parent=self)

    async def run_phase(self):
        prev_pin_values = self.vif.read_pins()

        while True:
            await ClockCycles(self.dut.clk, 5)

            await RisingEdge(self.dut.clk)
            await ReadOnly()
            curr_pin_values = self.vif.read_pins()

            self.logger.info(f"GPIO current pin values = {hex(curr_pin_values)}")

            if curr_pin_values != prev_pin_values:
                # Monitor the change
                tr = gpio_seq_item(name="gpio_mon_tr", value=curr_pin_values)
                
                # Broadcast the transaction
                self.ap.write(tr)

                self.logger.info(f"FLAG: GPIO values changed from {hex(prev_pin_values)} to {hex(curr_pin_values)}")

                prev_pin_values = curr_pin_values
