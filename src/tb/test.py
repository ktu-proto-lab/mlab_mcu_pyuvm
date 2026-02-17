import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, ClockCycles

@cocotb.test()
async def run_test(dut):
    """Initial test to verify connection"""
    
    cocotb.start_soon(Clock(dut.clk, 1, units="ns").start())

    dut._log.info("Starting simulation")
    
    dut.rst.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst.value = 1

    dut._log.info("Waiting for GPIO_PIN_0")
    await RisingEdge(dut.ext_pad_io[0])