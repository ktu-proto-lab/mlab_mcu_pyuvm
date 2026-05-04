import random
from seq.mcu_virtual_sequence import McuVirtualSequence
from seq.cli_cmd_item import *
from seq.uart_string_sequence import UartStringSequence
from uvc.uart_byte import UartByte

class CliCmdSequence(McuVirtualSequence):
    def __init__(self, name="CliCmdSequence"):
        super().__init__(name)

        self.cmds =[
            # CliCmdEchoItem,
            CliCmdMemWriteItem,
            CliCmdMemReadItem,
            CliCmdMemDumpItem,
            CliCmdMemCksumItem,
            CliCmdMemTestItem,
            CliCmdMemSizeItem,
            CliCmdGpioGetItem,
         ]

    async def body(self):
        await super().body()

        for _ in range(10):
            await self.wait_mcu_ready()
            cmd = self.make_random_cli_command()
            await self.send_command(cmd)

        await self.wait_mcu_ready()

    def make_random_cli_command(self) -> CliCmdItem:
        RandomCliCmdClass = random.choice(self.cmds)
        cmd: CliCmdItem = RandomCliCmdClass.create("cmd")
        cmd.cfg = self.cfg
        cmd.randomize()
        return cmd

    async def send_command(self, cmd: CliCmdItem):
        uart_string_sequence = UartStringSequence.create("req")
        uart_string_sequence.string = f"{cmd}\n"
        await uart_string_sequence.start(self.sequencer.uart)
        await self.wait_mcu_busy()

    async def wait_mcu_ready(self):
        self.sequencer.logger.debug("waiting mcu ready state event")
        await self.sequencer.event_pool.mcu_ready.wait()
        self.sequencer.event_pool.mcu_ready.clear()
        self.sequencer.logger.debug("awaited mcu ready state event")

    async def wait_mcu_busy(self):
        self.sequencer.logger.debug("waiting mcu busy state event")
        await self.sequencer.event_pool.mcu_busy.wait()
        self.sequencer.event_pool.mcu_busy.clear()
        self.sequencer.logger.debug("awaited mcu busy state event")
