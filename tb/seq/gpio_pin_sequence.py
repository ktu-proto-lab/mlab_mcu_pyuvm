from pyuvm import *
from uvc.gpio import GpioTransaction

class GpioPinSequence(uvm_sequence):
    async def body(self):
        for _ in range(10):
            req = GpioTransaction("req")
            await self.start_item(req)
            req.randomize()
            await self.finish_item(req)
