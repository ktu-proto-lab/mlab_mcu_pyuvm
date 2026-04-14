from seq.mcu_virtual_sequence import McuVirtualSequence
from seq.uart_string_sequence import UartStringSequence

class CmdMemSizeBasicSequence(McuVirtualSequence):
    def __init__(self, name="CmdMemSizeBasicSequence"):
        super().__init__(name)

    async def body(self):
        await super().body()

        header = "mem size"
        args = ["text", "data", "bss", "data", "text", "bss", "text"]

        for arg in args:
            self.sequencer.logger.debug("waiting mcu ready state event")
            await self.sequencer.event_pool.mcu_ready.wait()
            self.sequencer.event_pool.mcu_ready.clear()
            self.sequencer.logger.info(f"mcu is ready, driving basic '{header}' sequence")
            seq = UartStringSequence.create("seq")
            seq.string = f"{header} {arg}\n"
            await seq.start(self.sequencer.uart)
            self.sequencer.logger.info(f"drove '{seq.string}'")
            self.sequencer.logger.debug("waiting for mcu busy state event")
            await self.sequencer.event_pool.mcu_busy.wait()
            self.sequencer.event_pool.mcu_busy.clear()
            self.sequencer.logger.debug("mcu ready")
