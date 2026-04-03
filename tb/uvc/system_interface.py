from cocotb.handle import SimHandleBase
from cocotb.log import SimLog
from cocotb.triggers import RisingEdge, ClockCycles
from vif import McuVirtualInterface

class SystemInterface:
    def __init__(self, name="SystemInterface", parent=None):
        parent_name: str = parent.get_full_name() if hasattr(parent, "get_full_name") else "cocotb"
        full_name: str = f"{parent_name}.{name}"
        # TODO (refac): logger should be from uvm maybe?
        self.logger = SimLog(full_name)
        self.system_clock: SimHandleBase = None
        self.system_reset: SimHandleBase = None

    def map(self, vif: McuVirtualInterface):
        # TODO (debug): debug logs
        self.system_clock = vif.clock
        self.system_reset = vif.reset

    async def system_reset_done(self):
        await RisingEdge(self.system_reset)

    async def system_clock_cycle(self):
        await ClockCycles(signal=self.system_clock, num_cycles=1, rising=True)

    async def system_clock_cycles(self, num_cycles: int):
        await ClockCycles(signal=self.system_clock, num_cycles=num_cycles, rising=True)
