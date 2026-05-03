from seq.mcu_virtual_sequence import McuVirtualSequence
from seq.cli_cmd_item import CliCmdItem
from seq.uart_string_sequence import UartStringSequence
from uvc.uart_byte import UartByte

class CliCmdSequence(McuVirtualSequence):
    def __init__(self, name="CliCmdSequence"):
        super().__init__(name)

    async def body(self):
        await super().body()

        for _ in range(10):
            self.sequencer.logger.debug("waiting mcu ready state event")
            await self.sequencer.event_pool.mcu_ready.wait()
            # TODO: clear events at a certain stage to avoid clearing before others are waiting for it
            self.sequencer.event_pool.mcu_ready.clear()
            self.sequencer.logger.debug("awaited mcu ready state event")
            cmd: CliCmdItem = CliCmdItem.create("req")
            cmd.cfg = self.cfg
            cmd.randomize()
            uart_string_sequence: UartStringSequence = UartStringSequence.create("uart_string_sequence")
            uart_string_sequence.string = f"{cmd}\n"
            await uart_string_sequence.start(self.sequencer.uart)
            self.sequencer.logger.debug("waiting mcu busy state event")
            await self.sequencer.event_pool.mcu_busy.wait()
            self.sequencer.event_pool.mcu_busy.clear()
            self.sequencer.logger.debug("awaited mcu busy state event")

        await self.sequencer.event_pool.mcu_ready.wait()
        self.sequencer.event_pool.mcu_ready.clear()
