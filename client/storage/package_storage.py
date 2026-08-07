class PackageStorage:

    _lot_size = 0.01

    @classmethod
    def set_lot_size(cls, lot_size: float):
        cls._lot_size = lot_size

    @classmethod
    def get_lot_size(cls) -> float:
        return cls._lot_size