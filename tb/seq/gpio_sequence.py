from pyuvm import *
from uvc.gpio import GpioTransaction

class GpioSequence(uvm_sequence):
    async def body(self):
        for _ in range(10):
            req = GpioTransaction("req")
            req.randomize()
            await self.start_item(req)
            await self.finish_item(req)