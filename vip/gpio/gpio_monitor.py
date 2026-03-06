from pyuvm import *
from cocotb.triggers import ReadOnly, RisingEdge
from vip.gpio.gpio_if import gpio_if
from vip.gpio.gpio_sequence_item import gpio_sequence_item

class gpio_monitor(uvm_monitor):
    def build_phase(self):
        super().build_phase()

        self.vif: gpio_if = ConfigDB().get(context=self, inst_name="", field_name="vif")

        # Broadcast to the Scoreboard
        self.analysis_port = uvm_analysis_port(name="analysis_port", parent=self)
        
        self.logger.debug("build phase done")
        
    def sample(self) -> int:
        """
        @brief Template method for child Monitors to sample specific signals to be monitored
        """
        raise NotImplementedError
        # TODO: Maybe use this?
        uvm_not_implemented(header="", message="")

    async def run_phase(self):
        await super().run_phase()
        
        # Wait for system to boot up to avoid unresolvable gpio pin output values
        await RisingEdge(self.vif.rst)
        await ReadOnly()

        prev_val: int = self.sample()

        while True:
            await RisingEdge(self.vif.clk)
            await ReadOnly()
            
            curr_val: int = self.sample()
            
            if curr_val is None:
                self.logger.warning("monitoring GPIO value, got None")
                continue

            if curr_val != prev_val:
                # Monitor the change
                tr = gpio_sequence_item(name="gpio_mon_tr", value=curr_val)
                self.logger.debug(f"Value changed to {tr}")
                
                # Broadcast the transaction
                self.analysis_port.write(tr)

                prev_val = curr_val

class gpio_output_monitor(gpio_monitor):
    def sample(self) -> int:
        value: int = self.vif.read_enabled_output()

        if value is None:
            return None

        return value & 0xF0

class gpio_input_monitor(uvm_monitor):
    def build_phase(self):
        super().build_phase()
        
        # Subscribe to Driver's Analysis Port instead of sampling intermediate changing values directly from hardware
        self.driver_fifo = uvm_tlm_analysis_fifo(name="driver_fifo", parent=self)
        
        # Broadcast directly to the Scoreboard
        self.analysis_port = uvm_analysis_port(name="analysis_port", parent=self)
    
    async def run_phase(self):
        await super().run_phase()
        
        while True:
            tr: gpio_sequence_item = await self.driver_fifo.get()
            self.logger.debug(f"Got input item from the driver: {tr}")
            
            # Forward Driver's input to the Scoreboard
            self.analysis_port.write(tr)
