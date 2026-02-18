import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, ClockCycles, ReadOnly
from vif.gpio import gpio

@cocotb.test()
async def GPIO_PIN_0_test(dut):
    """ Verify GPIO connection """
    
    gpio_vif = gpio(dut)

    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    
    dut.rst.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst.value = 1

    dut._log.info("Waiting for GPIO_PIN_0 output")

    CLOCK_CYCLES = 100_000
    for i in range(200):

        await ClockCycles(dut.clk, CLOCK_CYCLES)
        await ReadOnly()

        if dut.ext_pad_io[0].value.integer == 1:
            dut._log.info(f"GPIO_PIN_0 = {gpio_vif.read_pin(0)}, GPIO pin values: {gpio_vif.read_pins_binsrt()}")
            assert gpio_vif.read_pin(0) == 1, f"GPIO values: {gpio_vif.read_pins_binsrt()}"
            return
        
        dut._log.info(f"After {i * CLOCK_CYCLES} I/O pad value: {gpio_vif.read_pins_binsrt()}")