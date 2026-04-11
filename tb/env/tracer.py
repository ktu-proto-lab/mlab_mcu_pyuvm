import cocotb
from pyuvm import uvm_component, uvm_tlm_analysis_fifo, ConfigDB, uvm_analysis_port

from errors import ConfigError, AsciiError
from uvc import UartByte

from env.config import Config

class Tracer(uvm_component):
    def __init__(self, name="Tracer", parent=None):
        super().__init__(name, parent)
        self.cfg: Config = None
        self.file = None
        
        self.uart_drv_fifo: uvm_tlm_analysis_fifo = None
        self.uart_in_ap: uvm_analysis_port = None
        self.uart_mon_fifo: uvm_tlm_analysis_fifo = None
        self.uart_out_ap: uvm_analysis_port = None
        
    def build_phase(self):
        super().build_phase()

        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigError("no configuration provided for tracer")
        
        self.cfg = ConfigDB().get(self, "", "cfg")
        
        self.file = open(self.cfg.tracer_file_path, "w")
        
        self.uart_drv_fifo = uvm_tlm_analysis_fifo.create("uart_drv_fifo", self)
        self.uart_in_ap = uvm_analysis_port.create("uart_in_ap", self)
        
        self.uart_mon_fifo = uvm_tlm_analysis_fifo.create("uart_mon_fifo", self)
        self.uart_out_ap = uvm_analysis_port.create("uart_out_ap", self)
        
    async def run_phase(self):
        await super().run_phase()
        
        cocotb.start_soon(self.uart_byte_stream(self.uart_drv_fifo, self.uart_in_ap, ">"))
        cocotb.start_soon(self.uart_byte_stream(self.uart_mon_fifo, self.uart_out_ap, "<"))
    
    async def uart_byte_stream(self, fifo: uvm_tlm_analysis_fifo, ap: uvm_analysis_port, prefix: str = ""):
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
                
    def final_phase(self):
        super().final_phase()
        
        self.file.close()
            