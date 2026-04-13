from pyuvm import uvm_component, ConfigDB, uvm_tlm_analysis_fifo
from errors import ConfigError
from env.mcu_config import McuConfig
from env.mcu_ref_model import McuRefModel

class McuScoreboard(uvm_component):
    def __init__(self, name="McuScoreboard", parent=None):
        super().__init__(name, parent)
        self.is_active: bool = None
        self.cfg: McuConfig = None
        self.ref_model: McuRefModel = None
        self.request_fifo: uvm_tlm_analysis_fifo = None
        self.actual_fifo: uvm_tlm_analysis_fifo = None
        self.expected_fifo: uvm_tlm_analysis_fifo = None

    def build_phase(self):
        super().build_phase()

        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigError(
                "no configuration provided for mcu scoreboard"
            )

        self.cfg = ConfigDB().get(self, "", "cfg")

        if not isinstance(self.cfg, McuConfig):
            raise ConfigError(
                f"provided configuration is not expected McuConfig type, provided {type(self.cfg).__name__}"
            )

        self.is_active = self.cfg.scoreboard_enable

        if not self.is_active:
            self.logger.info("scoreboard is disabled")
            return

        ConfigDB().set(self, "ref_model", "cfg", self.cfg)
        self.ref_model = McuRefModel.create("ref_model", self)

        self.request_fifo = uvm_tlm_analysis_fifo.create("req_fifo", self)
        self.actual_fifo = uvm_tlm_analysis_fifo.create("rsp_fifo", self)
        self.expected_fifo = uvm_tlm_analysis_fifo.create("expected_fifo", self)

    def connect_phase(self):
        super().connect_phase()
        self.ref_model.ap.connect(self.expected_fifo.analysis_export)

    async def run_phase(self):
        await super().run_phase()

        if not self.is_active:
            return

        while True:
            self.logger.debug("waiting request")
            request = await self.request_fifo.get()

            self.logger.debug("waiting expected response")
            expected = await self.expected_fifo.get()

            self.logger.debug("waiting actual response")
            actual = await self.actual_fifo.get()

            # TODO: check expected from reference model with actual
