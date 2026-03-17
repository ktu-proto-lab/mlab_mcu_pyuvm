from cocotb.handle import SimHandleBase
from cocotb.log import SimLog
from cocotb.triggers import RisingEdge, ClockCycles
from typing import cast
from vif import mcu_vif

class base_if:
    
    system_clock: SimHandleBase
    system_reset: SimHandleBase
    
    logger: SimLog
    
    def __init__(self, name="base_if", parent=None):
        parent_name: str = parent.get_full_name() if hasattr(parent, "get_full_name") else "cocotb"
        full_name: str = f"{parent_name}.{name}"
        self.logger = SimLog(full_name)
        
        self.system_clock = None
        self.system_reset = None
        
    def connect(self, dut: mcu_vif):
        self.system_clock = dut.clock
        self.system_reset = dut.reset
    
    async def system_reset_done(self):
        await RisingEdge(self.system_reset)
        
    async def system_clock_cycle(self):
        await ClockCycles(signal=self.system_clock, num_cycles=1, rising=True)

    async def system_clock_cycles(self, num_cycles: int):
        await ClockCycles(signal=self.system_clock, num_cycles=num_cycles, rising=True)
