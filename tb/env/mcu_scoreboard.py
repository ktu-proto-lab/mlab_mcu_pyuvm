from pyuvm import uvm_component, ConfigDB, uvm_tlm_analysis_fifo
from errors import ConfigTestError

from cfg.config import Config
from ref.mcu_transaction import McuTransaction

class McuScoreboard(uvm_component):
    def __init__(self, name="McuScoreboard", parent=None):
        super().__init__(name, parent)
        self.is_active: bool = None
        self.cfg: Config = None
        self.request_fifo: uvm_tlm_analysis_fifo = None
        self.actual_fifo: uvm_tlm_analysis_fifo = None
        self.expected_fifo: uvm_tlm_analysis_fifo = None
        self.successes: list[McuTransaction]  = []
        self.failures: list[McuTransaction]   = []
        self.passed: bool = True

    def build_phase(self):
        super().build_phase()

        if not ConfigDB().exists(self, "", "cfg"):
            raise ConfigTestError(
                "no configuration provided for mcu scoreboard"
            )

        self.cfg = ConfigDB().get(self, "", "cfg")

        if not isinstance(self.cfg, Config):
            raise ConfigTestError(
                f"provided configuration is not expected Config type, provided {type(self.cfg).__name__}"
            )

        self.is_active = self.cfg.scoreboard_enable

        if not self.is_active:
            self.logger.info("scoreboard is disabled")
            return

        self.request_fifo = uvm_tlm_analysis_fifo.create("req_fifo", self)
        self.actual_fifo = uvm_tlm_analysis_fifo.create("rsp_fifo", self)
        self.expected_fifo = uvm_tlm_analysis_fifo.create("expected_fifo", self)

    async def run_phase(self):
        await super().run_phase()

        if not self.is_active:
            return

        while True:

            scb_txn: McuTransaction = McuTransaction.create("actual_txn")

            self.logger.debug("waiting request")
            scb_txn.request: str = await self.request_fifo.get()

            self.logger.debug("waiting expected response")
            ref_txn: McuTransaction = await self.expected_fifo.get()

            if ref_txn.request != scb_txn.request:
                self.logger.error(
                    f"reference and scoreboard components have different requests, scoreboard got: '{scb_txn.request}', reference model got: '{ref_txn.request}'"
                )

            # continue checking, do not stop simulation
            scb_txn.expected = ref_txn.expected

            self.logger.debug("waiting actual response")
            scb_txn.actual: str = await self.actual_fifo.get()

            if scb_txn.expected == scb_txn.actual and scb_txn.request == ref_txn.request:
                self.logger.info(f"success ({scb_txn})")
                self.successes.append(scb_txn)
            else:
                self.logger.error(f"failure ({scb_txn})")
                self.failures.append(scb_txn)

    def check_phase(self):
        super().check_phase()

        if not self.is_active:
            return

        # TODO: write to file
        self.logger.info("--- SCOREBOARD ---")
        self.logger.info(f"| Total transactions: {len(self.failures) + len(self.successes)} |")
        self.logger.info(f"| Successes: {len(self.successes)} |")
        self.logger.info(f"| Failures:  {len(self.failures)} |")
        self.logger.info("------------------")

        if len(self.failures) > 0:
            self.logger.error("Failures:")
            self.passed = False

        for failure in self.failures:
            self.logger.error(failure)
