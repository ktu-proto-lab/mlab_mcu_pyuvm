from cocotb.handle import SimHandleBase
from cocotb.log import SimLog

class base_if:
    
    def __init__(self, dut: SimHandleBase, name="base_if", parent=None):
        self.system_clock: SimHandleBase = dut.clk
        self.system_reset: SimHandleBase = dut.rst
        
        parent_name = parent.get_full_name() if hasattr(parent, "get_full_name") else "cocotb"
        full_name = f"{parent_name}.{name}"
        self.logger = SimLog(full_name)