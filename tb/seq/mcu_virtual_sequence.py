from pyuvm import uvm_sequence, uvm_tlm_analysis_fifo
from env.mcu_virtual_sequencer import McuVirtualSequencer
from seq.uart_string_sequence import UartStringSequence
from uvc.uart import UartTransaction

class McuVirtualSequence(uvm_sequence):
    def __init__(self, name="McuVirtualSequence"):
        super().__init__(name)
        self.sequencer: McuVirtualSequencer = None
        self.uart_receive_fifo: uvm_tlm_analysis_fifo = None
    
    # TODO: check if the uart sequencer has vif connected
    async def receive_uart_string(self):
        string = ""
        self.sequencer.logger.debug("receiving uart string")
        while True:
            txn: UartTransaction = await self.uart_receive_fifo.get()
            char: chr = txn.to_ascii()
            if char == '\n' or char == '\0':
                break
            string += char
        self.sequencer.logger.debug(f"received {string} uart string")
        return string
            
    # TODO: this is a job for gpio pins, not uart, same with ready
    async def ack(self):
        self.sequencer.logger.info("waiting for acknowledgement")
        received_string = await self.receive_uart_string()
        assert received_string == "ack", f"expected acknowledgement string"
        self.sequencer.logger.info("acknowledgement received")
        
    async def ready(self):
        self.sequencer.logger.info("waiting for dut to be ready")
        received_string = await self.receive_uart_string()
        assert received_string == "ready", f"expected ready string"
        self.sequencer.logger.info("dut ready")
        
    async def send_uart_string(self, string: str):
        uart_string_sequence: UartStringSequence = UartStringSequence.create("uart_string_sequence")
        uart_string_sequence.set_string(string)
        self.sequencer.logger.info(f"sending {uart_string_sequence}")
        await self.sequencer.uart_sequencer.vif.enable_transmit()
        await uart_string_sequence.start(self.sequencer.uart_sequencer)
        await self.sequencer.uart_sequencer.vif.disable_transmit()
        self.sequencer.logger.info(f"sent {uart_string_sequence}")

