from pyuvm import *
from cocotb.triggers import ClockCycles, ReadOnly, RisingEdge
from cocotb.handle import SimHandleBase
from vif.gpio_if import gpio_if
from obj.gpio_seq_item import gpio_seq_item


class gpio_monitor(uvm_monitor):
    def build_phase(self):
        super().build_phase()

        self.vif: gpio_if = ConfigDB().get(context=self, inst_name="", field_name="vif")

        # Broadcast to the Scoreboard
        self.ap = uvm_analysis_port(name="ap", parent=self)

    async def run_phase(self):
        await RisingEdge(self.vif.clk)

        prev_pin_values = self.vif.read_pins()

        while True:
            await RisingEdge(self.vif.clk)
            await ReadOnly()
            
            curr_pin_values = self.vif.read_pins()

            if curr_pin_values != prev_pin_values:
                # Monitor the change
                tr = gpio_seq_item(name="gpio_mon_tr", value=curr_pin_values)
                
                # Broadcast the transaction
                self.ap.write(tr)

                self.logger.debug(f"GPIO values changed to {hex(curr_pin_values)}")

                prev_pin_values = curr_pin_values
