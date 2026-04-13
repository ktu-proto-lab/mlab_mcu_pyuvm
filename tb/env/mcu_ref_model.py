from pyuvm import uvm_component, uvm_analysis_port, uvm_tlm_analysis_fifo, ConfigDB
from env.mcu_config import McuConfig
from env.mcu_memory_mirror import McuMemoryMirror
from errors import ConfigError, NotImplementedError

# Maybe this needs to be a component too.
class McuRefModel(uvm_component):
    def __init__(self, name="McuRefModel", parent=None):
        super().__init__(name, parent)
        self.cfg: McuConfig = None
        self.memory: McuMemoryMirror = None
        self.req_fifo: uvm_tlm_analysis_fifo = None
        self.ap: uvm_analysis_port = None

    def build_phase(self):
        super().build_phase()

        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigError(
                "no configuration provided for mcu reference model"
            )

        self.cfg = ConfigDB().get(self, "", "cfg")

        if not isinstance(self.cfg, McuConfig):
            raise ConfigError(
                f"expected assigned configuration to be McuConfig, actual is {type(self.cfg).__name__}"
            )

        self.memory = McuMemoryMirror.create("memory")
        self.memory.source_filepath = self.cfg.mem_path
        self.memory.upload_source_binaries()
        self.logger.debug(f"created memory mirror from '{self.memory.source_filepath}'")

        self.req_fifo = uvm_tlm_analysis_fifo.create("req_fifo")
        self.ap = uvm_analysis_port.create("ap")

    async def run_phase(self):
        await super().run_phase()

        while True:
            req = await self.req_fifo.get()
            self.logger.debug(f"req: {req}")

            # TODO: process request and form predicted response
            rsp = "to be impemented"

            self.ap.write(rsp)
