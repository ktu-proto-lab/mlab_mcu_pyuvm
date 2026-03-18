from uvc.gpio.gpio_monitor import gpio_monitor

class gpio_input_monitor(gpio_monitor):
    def sample(self) -> int:
        value: int = self.vif.read_input(self.mask)
        return value
