from pyuvm import uvm_component, uvm_analysis_port, uvm_tlm_analysis_fifo, ConfigDB
from env import McuConfig
from errors import ConfigError, NotImplementedError
from ref.mcu_memory_mirror import McuMemoryMirror
from ref.mcu_cli_interpreter import McuCliInterpreter

# Maybe this needs to be a component too.
class McuRefModel(uvm_component):
    def __init__(self, name="McuRefModel", parent=None):
        super().__init__(name, parent)
        self.cfg: McuConfig = None
        self.memory: McuMemoryMirror = None
        self.cli: McuCliInterpreter = None
        self.request_fifo: uvm_tlm_analysis_fifo = None
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
        self.memory.cfg = self.cfg.mem_cfg
        self.memory.upload_source_binaries()
        self.logger.debug(f"created memory mirror from '{self.memory.cfg.source_build_dir_path}'")

        self.cli = McuCliInterpreter.create("cli")
        self.cli.memory = self.memory
        self.logger.debug("created cli and assigned memory mirror")

        self.request_fifo = uvm_tlm_analysis_fifo.create("req_fifo", self)
        self.ap = uvm_analysis_port.create("ap", self)

        self.logger.debug("mcu reference model build phase done")

    async def run_phase(self):
        await super().run_phase()

        while True:
            req: str = await self.request_fifo.get()
            self.logger.info(f"req: '{req}'")

            rsp: str = self.predict(req)

            self.ap.write(rsp)
            self.logger.info(f"rsp: '{rsp}'")

    def predict(self, req: str) -> str:
        return self.cli.execute(req)
