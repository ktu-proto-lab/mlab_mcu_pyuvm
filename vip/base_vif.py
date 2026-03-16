from cocotb.handle import SimHandleBase
from cocotb.log import SimLog
from cocotb.triggers import RisingEdge, ClockCycles
from typing import cast
from vip.mcu import mcu

class base_vif:
    
    system_clock: SimHandleBase
    system_reset: SimHandleBase
    
    logger: SimLog
    
    def __init__(self, dut: mcu, name="base_if", parent=None):
        self.system_clock = cast(SimHandleBase, dut.clock)
        self.system_reset = cast(SimHandleBase, dut.reset)
        
        parent_name: str = parent.get_full_name() if hasattr(parent, "get_full_name") else "cocotb"
        full_name: str = f"{parent_name}.{name}"
        self.logger = SimLog(full_name)
        
    async def system_reset_done(self):
        await RisingEdge(self.system_reset)
        
    async def system_clock_cycle(self):
        await ClockCycles(signal=self.system_clock, num_cycles=1, rising=True)

    async def system_clock_cycles(self, num_cycles: int):
        await ClockCycles(signal=self.system_clock, num_cycles=num_cycles, rising=True)
