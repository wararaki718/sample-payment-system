class InventoryRepository:
    # In-memory stock for demo purposes.
    _stock: dict[str, int] = {
        "SKU-APPLE": 10,
        "SKU-BANANA": 20,
        "SKU-COFFEE": 5,
    }

    def has_stock(self, sku: str, quantity: int) -> bool:
        return self._stock.get(sku, 0) >= quantity

    def decrease(self, sku: str, quantity: int) -> None:
        current = self._stock.get(sku, 0)
        self._stock[sku] = current - quantity

    def available_skus(self) -> list[str]:
        return sorted(self._stock.keys())
