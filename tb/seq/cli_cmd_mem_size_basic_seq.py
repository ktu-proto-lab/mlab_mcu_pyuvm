from seq.mcu_virtual_sequence import McuVirtualSequence
from seq.uart_string_sequence import UartStringSequence

class CliCmdMemSizeBasicSeq(McuVirtualSequence):
    def __init__(self, name="CliCmdMemSizeBasicSeq"):
        super().__init__(name)

    async def body(self):
        await super().body()

        header = "mem size"
        args = ["text", "data", "bss", "ram", "instr", "bin", "dmem", "imem", "stack", "x"]

        for arg in args:
            self.sequencer.logger.debug("waiting mcu ready state event")
            await self.sequencer.event_pool.mcu_ready.wait()
            self.sequencer.event_pool.mcu_ready.clear()
            self.sequencer.logger.debug(f"mcu is ready, driving basic '{header}' sequence")
            seq = UartStringSequence.create("seq")
            cmd = f"{header} {arg}"
            seq.string = f"{cmd}\n"
            await seq.start(self.sequencer.uart)
            self.sequencer.logger.debug(f"req: '{cmd}'")
            self.sequencer.logger.debug("waiting for mcu busy state event")
            await self.sequencer.event_pool.mcu_busy.wait()
            self.sequencer.event_pool.mcu_busy.clear()
            self.sequencer.logger.debug("mcu busy")

        await self.sequencer.event_pool.mcu_ready.wait()
        self.sequencer.event_pool.mcu_ready.clear()
