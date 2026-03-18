from uvc.gpio.gpio_monitor import gpio_monitor

class gpio_output_monitor(gpio_monitor):
    def sample(self) -> int:
        value: int = self.vif.read_output(self.mask)
        return value
