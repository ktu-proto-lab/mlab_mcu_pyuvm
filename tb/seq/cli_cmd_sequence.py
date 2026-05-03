import random
from seq.mcu_virtual_sequence import McuVirtualSequence
from seq.cli_cmd_item import *
from seq.uart_string_sequence import UartStringSequence
from uvc.uart_byte import UartByte

class CliCmdSequence(McuVirtualSequence):
    def __init__(self, name="CliCmdSequence"):
        super().__init__(name)
        self.cmds = [
             (CliCmdMemWriteItem, 100)
         ]

    async def body(self):
        await super().body()

        for _ in range(10):
            await self.mcu_ready()
            cmd = self.make_random_cli_command()
            await self.send_command(cmd)

        await self.mcu_done()

    def make_random_cli_command(self) -> CliCmdItem:
        cmd_classes, cmd_weights = zip(*self.cmds)
        RandomCliCmdClass = random.choices(cmd_classes, cmd_weights, k=1)[0]
        cmd: CliCmdItem = RandomCliCmdClass.create("cmd")
        cmd.cfg = self.cfg
        cmd.randomize()
        return cmd

    async def send_command(self, cmd: CliCmdItem):
        uart_string_sequence = UartStringSequence.create("req")
        uart_string_sequence.string = f"{cmd}\n"
        await uart_string_sequence.start(self.sequencer.uart)
        await self.mcu_done()


    async def mcu_ready(self):
        self.sequencer.logger.debug("waiting mcu ready state event")
        await self.sequencer.event_pool.mcu_ready.wait()
        # TODO: clear events at a certain stage to avoid clearing before others are waiting for it
        self.sequencer.event_pool.mcu_ready.clear()
        self.sequencer.logger.debug("awaited mcu ready state event")

    async def mcu_done(self):
        await self.sequencer.event_pool.mcu_ready.wait()
        self.sequencer.event_pool.mcu_ready.clear()

    async def mcu_done(self):
        self.sequencer.logger.debug("waiting mcu busy state event")
        await self.sequencer.event_pool.mcu_busy.wait()
        self.sequencer.event_pool.mcu_busy.clear()
        self.sequencer.logger.debug("awaited mcu busy state event")
