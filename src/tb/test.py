import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge

@cocotb.test()
async def run_test(dut):
    """Initial test to verify connection"""
    
    cocotb.start_soon(Clock(dut.clk_sys, 12.5, units="ns").start())

    dut._log.info("Starting simulation from cocotb.")
    
    dut.rst_sys_n.value = 0
    await Timer(100, units="ns")
    dut.rst_sys_n.value = 1
    
    for i in range(5):
        await RisingEdge(dut.clk_sys)
        dut._log.info(f"Clock cycle {i} reached")

    await Timer(100, units="ns")
    dut._log.info("Simulation finished")