from seq.mcu_virtual_sequence import McuVirtualSequence
from seq.cli_mem_transaction import CliMemTransaction

class CliMemSequence(McuVirtualSequence):
    
    async def send_command(self):
        pass
    
    async def response(self):
        pass
    
    async def body(self):
        await super().body()
        await self.ack()
        for _ in range(1):
            self.sequencer.logger.debug("forming request")
            req: CliMemTransaction = CliMemTransaction.create("req")
            self.sequencer.logger.debug("request formed")
            # await self.start_item(req)
            self.sequencer.logger.debug("randomizing request")
            req.randomize()
            self.sequencer.logger.debug("randomized cli mem transaction")
            # await self.finish_item(req)
            self.sequencer.logger.debug(f"sending via uart randomized command string '{req}'")
            await self.send_uart_string(req.to_string())
            self.sequencer.logger.debug(f"{req} sent, receiving response")
            await self.receive_uart_string()
            self.sequencer.logger.debug("waiting for mcu to be ready")
            await self.ready()
            self.sequencer.logger.debug("request item finished")
