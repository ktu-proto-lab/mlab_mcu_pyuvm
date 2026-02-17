import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, ClockCycles, ReadOnly

@cocotb.test()
async def GPIO_PIN_0_test(dut):
    """Wait for GPIO_PIN_0 output to verify connection"""
    
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    
    dut.rst.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst.value = 1

    dut._log.info("Waiting for GPIO_PIN_0 output")
    for i in range(200):
        CLOCK_CYCLES = 100_000
        await ClockCycles(dut.clk, CLOCK_CYCLES)
        await ReadOnly()
        dut._log.info(f"After {i * CLOCK_CYCLES} I/O pad value: {dut.ext_pad_io.value.binstr}")


    dut._log.info("Awaiting for GPIO_PIN_0 output indefinetelly...")
    await RisingEdge(dut.ext_pad_io[0])
    await ReadOnly()
    assert dut.ext_pad_io[0].value.integer == 1