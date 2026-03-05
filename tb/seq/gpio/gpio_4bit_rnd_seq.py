from pyuvm import *
from obj.gpio_seq_item import gpio_seq_item

class gpio_4bit_rnd_seq(uvm_sequence):
    async def body(self):
        
        for _ in range(1000):
            req = gpio_seq_item("req")
            
            req.randomize()
            
            # Send Request to Driver
            await self.start_item(req)
            await self.finish_item(req)