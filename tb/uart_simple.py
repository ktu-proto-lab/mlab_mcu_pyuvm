import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
from vip.uart.vif import uart_if

@cocotb.test
async def simple_uart_heartbeat_test(dut):
    
    cocotb.start_soon(Clock(dut.clk, 12.5, units='ns').start())
    dut._log.info(f"clock started")
    
    dut.rst.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst.value = 1
    dut._log.info(f"applied system reset")
    
    uart = uart_if(dut)
    
    uart.enable_transmit()
    dut._log.info(f"enabled uart transmit")
    
    # await ClockCycles(dut.clk, 20_000)
    
    
    expected = "hello uart"
    received = ""
    
    for _ in range(len(expected)):
        dut._log.info(f"waiting to receive byte")
        
        byte = await uart.receive_byte()
        
        dut._log.info(f"byte received {hex(byte)}")
        
        received += chr(byte)
        
    dut._log.info(f"received: {received}, expected: {expected}")

    send_string = "hello back"
    dut._log.info(f"transmitting: {send_string}")
    for byte in send_string:
        dut._log.info(f"transmitting {hex(ord(byte))}")
        await uart.transmit_byte(ord(byte))
        dut._log.info("transmitted")
    dut._log.info(f"transmitted: {send_string}")
    
    #await ClockCycles(dut.clk, 500)
    
    expected = "rodger that"
    received = ""
    
    dut._log.info(f"waiting for response")
    for _ in range(len(expected)):
        dut._log.info(f"waiting to receive byte")
        byte = await uart.receive_byte()
        dut._log.info(f"byte received {hex(byte)}")
        received += chr(byte)
        
    dut._log.info(f"response received: {received}")
    
        
    