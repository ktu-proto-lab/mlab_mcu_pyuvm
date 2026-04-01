import pyuvm
from pyuvm import ConfigDB, uvm_tlm_analysis_fifo
from uvc.uart import uart_if, uart_char_item
from test.base_test import base_test
from env.uart import uart_simple_env, uart_simple_env_config
from seq import uart_string_sequence

@pyuvm.test()
class cli_cmd_echo_simple_test(base_test):
    def build_phase(self):
        super().build_phase()
        
        self.vif = uart_if("vif", self)
        self.vif.wire(self.vif)
        
        self.env_cfg: uart_simple_env_config = uart_simple_env_config.create("env_cfg")
        self.env_cfg.vif = self.vif
        self.env_cfg.is_set = True
        ConfigDB().set(self, "env", "cfg", self.env_cfg)
        
        self.env: uart_simple_env = uart_simple_env.create("env", self)
        
        self.receive_fifo: uvm_tlm_analysis_fifo = uvm_tlm_analysis_fifo.create("receive_fifo", self)
        
    def connect_phase(self):
        super().connect_phase()

        self.env.agent.receive_analysis_port.connect(self.receive_fifo.analysis_export)
        
    async def run_phase(self):
        self.raise_objection()
        await super().run_phase()

        ack_expected = "ack\0"
        self.logger.debug(f"waiting for dut's acknowledgement message '{ack_expected}'")
        ack_actual = await self.receive_string()
        self.logger.debug(f"received ack message: {ack_actual}")
        
        assert (ack_expected == ack_actual),(
            f"expected ack message {ack_expected}, actual = {ack_actual}"
        )
        
        expected_received_string = "mlab mcu 2026"
        
        echo_transmit_string_sequence: uart_string_sequence = uart_string_sequence.create("echo_sequence")
        echo_transmit_string_sequence.string = f"echo \"{expected_received_string}\"\0";
        self.logger.debug(f"transmitting: {echo_transmit_string_sequence}")
        self.vif.enable_transmit()
        await echo_transmit_string_sequence.start(self.env.agent.sequencer)
        self.vif.disable_transmit()
        self.logger.info(f"transmitted {echo_transmit_string_sequence}")
        
        self.logger.debug("waiting echo response")
        self.receive_fifo.flush()
        actual_received_string = await self.receive_string()
        self.logger.info(f"received '{actual_received_string}'")
        
        assert (
            f"{expected_received_string}\0" == actual_received_string
                ),( 
            "echoed strings do not match: " 
            f"transmitted = {echo_transmit_string_sequence},"
            f"expected = '{expected_received_string}' actual = '{actual_received_string}'"
        )
        
        self.drop_objection()


    async def receive_string(self) -> str:
        string = ""
                
        while True:
            character: uart_char_item = await self.receive_fifo.get()
            string += character.char_value()
            if character.is_null_terminator():
                break;
            
        return string
            