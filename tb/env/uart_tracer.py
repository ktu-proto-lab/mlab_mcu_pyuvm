import cocotb
from pyuvm import uvm_component, uvm_object, ConfigDB, uvm_tlm_analysis_fifo, uvm_analysis_export
from error import ConfigError, UartAsciiError
from uvc.uart import UartTransaction

# tail -f sim/sim_build/uart_trace.log
# watch -n 0.1 'tail -n 5 sim/sim_build/uart_trace.log;' 
class UartTracer(uvm_component):
    class Config(uvm_object):
        def __init__(self, name="UartTracerConfig"):
            super().__init__(name)
            self.is_active: bool = True
            self.enable_transmit_stream: bool = True
            self.enable_receive_stream: bool = True
            self.file_path: str = "sim_build/uart_trace.log"
    
    def __init__(self, name="UartTracer", parent=None):
        super().__init__(name, parent)
        self.cfg: UartTracer.Config = None
        self.file = None
        self.transmit_fifo: uvm_tlm_analysis_fifo = None
        self.receive_fifo: uvm_tlm_analysis_fifo = None
        self.transmit_export: uvm_analysis_export = None
        self.receive_export: uvm_analysis_export = None

    def build_phase(self):
        super().build_phase()
        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigError("no configuration provided for uart tracer", self)
        self.cfg = ConfigDB().get(self, "", "cfg")
        if not self.cfg.is_active:
            self.logger.info("uart tracer is not active")
            return
        self.file = open(self.cfg.file_path, "w")
        self.logger.debug(f"opened {self.cfg.file_path} for trace streams")
        self.transmit_fifo = uvm_tlm_analysis_fifo.create("transmit_fifo", self)
        self.receive_fifo = uvm_tlm_analysis_fifo.create("receive_fifo", self)
        self.transmit_export = self.transmit_fifo.analysis_export
        self.receive_export = self.receive_fifo.analysis_export
        
    async def run_phase(self):
        await super().run_phase()
        if not self.cfg.is_active:
            return
        cocotb.start_soon(self.stream(self.transmit_fifo, prefix=">"))
        cocotb.start_soon(self.stream(self.receive_fifo, prefix="<"))
        
    async def stream(self, fifo: uvm_tlm_analysis_fifo, prefix: str = ""):
        buffer = ""
        while True:
            txn: UartTransaction = await fifo.get()
            if txn.is_idle_byte():
                continue
            try:
                char = txn.to_ascii()
            except UartAsciiError:
                self.logger.warning(f"received non ascii byte {txn.hex_value()}")
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
        if not self.cfg.is_active:
            return
        if self.file:
            self.file.close()
