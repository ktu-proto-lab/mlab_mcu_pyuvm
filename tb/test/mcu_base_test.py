from pyuvm import ConfigDB
from env.mcu import mcu_env, mcu_env_config
from uvc.gpio import gpio_config, gpio_if, gpio_monitor_config, gpio_driver_config
from uvc.uart import uart_config, uart_if
from test.base_test import base_test

class mcu_base_test(base_test):
    def __init__(self, name="mcu_base_test", parent=None):
        super().__init__(name, parent)
        self.cfg: mcu_env_config = None
        self.env: mcu_env = None
    
    def build_phase(self):
        super().build_phase()
        self.cfg = mcu_env_config.create("cfg")
        self.cfg.vif = self.mcu_vif
        self.cfg.gpio_enable = True
        self.cfg.uart_enable = True
        self.cfg.i2c_enable = False # TODO: implement I2C Agent
        self.cfg.gpio_cfg = gpio_config.create("gpio_cfg")
        self.cfg.gpio_cfg.vif = gpio_if("vif", self)
        self.cfg.gpio_cfg.vif.wire(self.cfg.vif)
        self.cfg.gpio_cfg.is_active = True
        self.cfg.gpio_cfg.monitor_cfg = gpio_monitor_config.create("cfg")
        self.cfg.gpio_cfg.port_type = gpio_config.port_type_enum.NONE
        self.cfg.gpio_cfg.driver_cfg = gpio_driver_config.create("cfg")
        self.cfg.gpio_cfg.monitor_cfg.mask = 0xFF
        self.cfg.gpio_cfg.driver_cfg.mask = 0x0F
        self.cfg.uart_cfg = uart_config.create("uart_cfg")
        ConfigDB().set(self, "env", "cfg", self.cfg)
        self.env = mcu_env.create("env", self)
        
    async def run_phase(self):
        self.raise_objection()
        await super().run_phase()
        self.drop_objection()
