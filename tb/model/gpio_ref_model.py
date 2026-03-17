class gpio_mirror_ref_model:
    def predict(self, input_value: int) -> int:
        return (input_value & 0x0F) << 4