class Point:
    def __init__(self, bit=0, check=False) -> None:
        """Class for describing points of a qr code matrix.

        Args:
            bit (int, optional): Bit value (1 or 0). Defaults to 0.
            check (bool, optional): Position value (busy or not).Defaults
            to False.
        """
        self.bit = bit
        self.check = check
