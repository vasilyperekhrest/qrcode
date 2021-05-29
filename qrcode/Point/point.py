class Point:
    def __init__(
            self,
            bit: bool = False,
            is_service_bit: bool = False,
            is_pattern: bool = False
    ) -> None:
        """Class for describing points of a qr code matrix.

        Args:
            bit: Bit value (1 or 0). Defaults to 0 (False).
            is_service_bit: Is it a service beat or not.
        """
        self.bit = bit
        self.is_service_bit = is_service_bit
        self.is_pattern = is_pattern
