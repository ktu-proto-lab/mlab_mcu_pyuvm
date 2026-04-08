from seq.mcu_virtual_sequence import McuVirtualSequence

class CliMemSequence(McuVirtualSequence):
    
    async def send_command(self):
        pass
    
    async def response(self):
        pass
    
    async def body(self):
        await super().body()
        await self.ack()
        # TODO (feat): these strings are CliMemTransaction (sequence items)
        await self.send_uart_string("mem read 0x80000006")
        await self.receive_uart_string()
        await self.ready()
        await self.send_uart_string("mem write 0x80001990 0xffffffff")
        await self.receive_uart_string()
        await self.ready()
        await self.send_uart_string("mem read 0x80001990")
        await self.receive_uart_string()
        await self.ready()
        await self.send_uart_string("mem cksum 0x80000000 0xff")
        await self.receive_uart_string()
        await self.ready()
        await self.send_uart_string("mem cksum 0x80000000 0x798")
        await self.receive_uart_string()
        await self.ready()
        await self.send_uart_string("mem cmd <arg1> <arg2>")
        await self.receive_uart_string()
        await self.ready()
        await self.send_uart_string("mem dump 0x80000300 0x3")
        await self.receive_uart_string()
        await self.ready()
