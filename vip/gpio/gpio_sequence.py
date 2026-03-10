from pyuvm import *
from vip.gpio.gpio_sequence_item import gpio_sequence_item

class gpio_4bit_random_sequence(uvm_sequence):
    async def body(self):
        
        for _ in range(10):
            req = gpio_sequence_item("req")
            
            req.randomize()
            
            # Send Request to Driver
            await self.start_item(req)
            await self.finish_item(req)