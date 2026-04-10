from pyuvm import uvm_component, uvm_tlm_analysis_fifo

class McuScoreboard(uvm_component):
    def __init__(self, name="McuScoreboard", parent=None):
        super().__init__(name, parent)
        self.expected_fifo: uvm_tlm_analysis_fifo = None
        self.actual_fifo: uvm_tlm_analysis_fifo = None
        # can be a touple of expected and actual
        self.successes = 0
        self.failures = 0
        
    def build_phase(self):
        super().build_phase()
        self.expected_fifo = uvm_tlm_analysis_fifo.create("expected_fifo", self)
        self.actual_fifo = uvm_tlm_analysis_fifo.create("actual_fifo", self)
        
    async def run_phase(self):
        await super().run_phase()
        while(True):
            actual = await self.actual_fifo.get()
            self.logger.info("waiting expected input")
            expected = await self.expected_fifo.get()
            self.logger.info("got expected input")
            if expected != actual:
                self.logger.error(f"expected: {expected}, actual: {actual}")
                self.failures += 1
            else:
                self.successes += 1

    def check_phase(self):
        super().check_phase()
        self.logger.info(f"successes: {self.successes}, failures {self.failures}")
        # TODO: assert
