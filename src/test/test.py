import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge

@cocotb.test()
async def run_test(dut):
    """Initial test to verify connection"""
    
    # Start the clock (Match the name 'clk_sys' from your wrapper)
    # 12.5ns = 80MHz
    cocotb.start_soon(Clock(dut.clk_sys, 12.5, units="ns").start())

    dut._log.info("Starting simulation with cocotb!")
    
    # Reset sequence (Match 'rst_sys_n' from your wrapper)
    dut.rst_sys_n.value = 0
    await Timer(100, units="ns")
    dut.rst_sys_n.value = 1
    
    # Wait for a few clock cycles
    for i in range(5):
        await RisingEdge(dut.clk_sys)
        dut._log.info(f"Clock cycle {i} reached")

    await Timer(100, units="ns")
    dut._log.info("Simulation finished")