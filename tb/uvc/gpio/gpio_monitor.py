from pyuvm import *
from cocotb.triggers import ReadOnly, RisingEdge
from uvc.gpio.gpio_sequence_item import gpio_sequence_item
from uvc.gpio.gpio_monitor_config import gpio_monitor_config
from uvc.gpio.gpio_if import gpio_if

class gpio_monitor(uvm_monitor):
    cfg: gpio_monitor_config
    vif: gpio_if
    mask: int
    analysis_port: uvm_analysis_port
    
    def build_phase(self):
        super().build_phase()

        if not ConfigDB().exists(self, "", "cfg"):
            self.logger.error("can not build without configuration")
        
        self.cfg = ConfigDB().get(self, "", "cfg")

        self.vif = self.cfg.vif

        self.mask = self.cfg.mask

        # Broadcast to the Scoreboard
        self.analysis_port = uvm_analysis_port(name="analysis_port", parent=self)
        
    def sample(self) -> int:
        """
        @brief Template method for child Monitors to sample specific signals to be monitored
        """
        raise NotImplementedError

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
                continue

            if curr_val != prev_val:
                # Monitor the change
                tr = gpio_sequence_item(name="gpio_mon_tr", value=curr_val)
                self.logger.debug(f"Value changed to {tr}")
                
                # Broadcast the transaction
                self.analysis_port.write(tr)

                prev_val = curr_val
