from pyuvm import uvm_component, uvm_analysis_port, uvm_tlm_analysis_fifo, ConfigDB
from errors import ConfigTestError, NotImplementedTestError, McuCliTestError, McuTestError

from cfg.config import Config
from ref.mcu_memory_mirror import McuMemoryMirror
from ref.mcu_cli_interpreter import McuCliInterpreter
from ref.mcu_transaction import McuTransaction
from ref.mcu_gpio_pad_state import McuGpioPadState

# Maybe this needs to be a component too.
class McuRefModel(uvm_component):
    def __init__(self, name="McuRefModel", parent=None):
        super().__init__(name, parent)
        self.cfg: Config = None
        self.memory: McuMemoryMirror = None
        self.cli: McuCliInterpreter = None
        self.request_fifo: uvm_tlm_analysis_fifo = None
        self.ap: uvm_analysis_port = None

    def build_phase(self):
        super().build_phase()

        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigTestError(
                "no configuration provided for mcu reference model"
            )

        self.cfg = ConfigDB().get(self, "", "cfg")

        if not isinstance(self.cfg, Config):
            raise ConfigTestError(
                f"expected assigned configuration to be Config, actual is {type(self.cfg).__name__}"
            )

        self.memory = McuMemoryMirror.create("memory")
        self.memory.cfg = self.cfg.mem_cfg
        self.memory.upload_source_binaries()
        self.logger.debug(f"created memory mirror from '{self.memory.cfg.source_build_dir_path}'")

        self.cli = McuCliInterpreter.create("cli")
        self.cli.memory = self.memory
        self.logger.debug("created cli and assigned memory mirror")
        # connected in env connect phase (needs gpio monitor ap)
        self.cli.gpio_state = McuGpioPadState.create("gpio_state")
        self.cli.gpio_state.cfg = self.cfg

        self.request_fifo = uvm_tlm_analysis_fifo.create("req_fifo", self)
        self.ap = uvm_analysis_port.create("ap", self)

        self.logger.debug("mcu reference model build phase done")

    async def run_phase(self):
        await super().run_phase()

        while True:
            txn: McuTransaction = McuTransaction.create("txn")

            txn.request: str = await self.request_fifo.get()
            self.logger.debug(f"request = '{txn.request}'")

            txn.expected: str = self.predict(txn.request)
            self.logger.debug(f"expected = '{txn.actual}'")

            self.ap.write(txn)

    def predict(self, req: str) -> str:
        try:
            return self.cli.execute(req)

        # do not stop whole simulation just because cli throws an error
        except McuTestError as e:
            self.logger.error(f"cli error '{e}'")
            return "mcu cli error"
