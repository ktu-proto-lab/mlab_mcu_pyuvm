from uvc.gpio.gpio_monitor import gpio_monitor

class gpio_output_monitor(gpio_monitor):
    def sample(self) -> int:
        # TODO: change to raw output
        value: int = self.vif.read_enabled_output()
        return value