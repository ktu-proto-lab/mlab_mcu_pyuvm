from cocotb.handle import SimHandleBase
from cocotb.log import SimLog
from cocotb.triggers import RisingEdge, ReadOnly, ClockCycles

class base_if:
    
    def __init__(self, dut: SimHandleBase, name="base_if", parent=None):
        self.system_clock: SimHandleBase = dut.clk
        self.system_reset: SimHandleBase = dut.rst
        
        parent_name = parent.get_full_name() if hasattr(parent, "get_full_name") else "cocotb"
        full_name = f"{parent_name}.{name}"
        self.logger = SimLog(full_name)
        
    async def system_reset_done(self):
        await RisingEdge(self.system_reset)
        
    async def system_clock_cycle(self):
        await ClockCycles(signal=self.system_clock, num_cycles=1, rising=True)

    async def system_clock_cycles(self, num_cycles: int):
        await ClockCycles(signal=self.system_clock, num_cycles=num_cycles, rising=True)
