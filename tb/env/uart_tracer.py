from pyuvm import uvm_subscriber, uvm_object, ConfigDB
from log.error import ConfigError, UartAsciiError
from uvc.uart import UartTransaction

# tail -f sim/sim_build/uart_trace.log
# watch -n 0.1 'tail -n 5 sim/sim_build/uart_trace.log;' 
class UartTracer(uvm_subscriber):
    class Config(uvm_object):
        def __init__(self, name="UartTracerConfig"):
            super().__init__(name)
            self.is_active: bool = True
            self.file_path: str = "sim_build/uart_trace.log"
    
    def __init__(self, name="UartTracer", parent=None):
        super().__init__(name, parent)
        self.cfg: UartTracer.Config = None
        self.file = None
        self.buffer = None

    def build_phase(self):
        super().build_phase()
        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigError("no configuration provided for uart tracer", self)
        self.cfg = ConfigDB().get(self, "", "cfg")
        if not self.cfg.is_active:
            self.logger.info("uart tracer is not active")
            return
        self.file = open(self.cfg.file_path, "w")
        self.buffer = ""
        
    def write(self, txn: UartTransaction):
        if not self.cfg.is_active:
            return
        
        try:
            char: chr = txn.to_ascii()
        except UartAsciiError:
            self.logger.warning(f"failed to convert uart transaction byte value '{txn.hex_value()}' to ascii character")
            # TODO: wtf???
            if txn.byte != 0xff:
                return
            char: chr = '\n'
        
        if char == '\n':
            if self.buffer == "":
                return
            self.file.write(f"< {self.buffer}\n")
            self.file.flush()
            self.buffer = ""
        else:
            self.buffer += char
    
    def final_phase(self):
        super().final_phase()
        if not self.cfg.is_active:
            return
        if self.file:
            self.file.close()
