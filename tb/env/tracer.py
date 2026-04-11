import cocotb
from pyuvm import uvm_component, uvm_tlm_analysis_fifo, ConfigDB, uvm_analysis_port

from errors import ConfigError, AsciiError
from uvc import UartByte, GpioPad

from env.config import Config

# watch -n 0.1 'tail -n 10 sim/sim_build/tracer.log;' 
class Tracer(uvm_component):
    def __init__(self, name="Tracer", parent=None):
        super().__init__(name, parent)
        self.cfg: Config = None
        self.file = None
        self.gpio_pad_fifo: uvm_tlm_analysis_fifo = None
        self.uart_rx_fifo: uvm_tlm_analysis_fifo = None
        self.uart_tx_fifo: uvm_tlm_analysis_fifo = None
        
    def build_phase(self):
        super().build_phase()

        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigError("no configuration provided for tracer")
        
        self.cfg = ConfigDB().get(self, "", "cfg")
        
        self.file = open(self.cfg.tracer_file_path, "w")

        self.gpio_pad_fifo = uvm_tlm_analysis_fifo.create("gpio_pad_fifo", self)
        
        self.uart_rx_fifo = uvm_tlm_analysis_fifo.create("uart_rx_fifo", self)
        self.uart_tx_fifo = uvm_tlm_analysis_fifo.create("uart_tx_fifo", self)
        
    async def run_phase(self):
        await super().run_phase()
        
        cocotb.start_soon(self.uart_byte_stream(self.uart_rx_fifo, ">"))
        cocotb.start_soon(self.uart_byte_stream(self.uart_tx_fifo, "<"))
    
    async def uart_byte_stream(self, fifo: uvm_tlm_analysis_fifo, prefix: str = ""):
        buffer = ""
        
        while True:
            byte: UartByte = await fifo.get()
            
            if not isinstance(byte, UartByte):
                raise TypeError(f"tracer receives uart bytes for stream, expected UartByte, got {type(byte).__name__}")
            
            try:
                char = byte.to_ascii()
            except AsciiError:
                self.logger.error(f"received non ascii byte {byte.hex_value()}")
                continue
            
            if char == '\n' or char == '\0':
                if buffer != "":
                    self.file.write(f"{prefix} {buffer}\n")
                    self.file.flush()
                    buffer = ""
            else:
                buffer += char
                
    async def gpio_pad_state(self, fifo: uvm_tlm_analysis_fifo):

        while True:
            gpio_pad_val: GpioPad = await fifo.get()
            
            if not isinstance(gpio_pad_val, GpioPad):
                raise TypeError(f"tracer receives gpio pad state value, expected GpioPad, got {type(gpio_pad_val).__name__}")
               
            self.file.write(f"[] {gpio_pad_val}")
                
    def final_phase(self):
        super().final_phase()
        
        self.file.close()
            