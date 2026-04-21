from src.modules.inventory.internal.inventory_repository import InventoryRepository


class InventoryService:
    def __init__(self) -> None:
        self._repo = InventoryRepository()

    def reserve(self, sku: str, quantity: int) -> None:
        if not self._repo.has_stock(sku, quantity):
            available = ", ".join(self._repo.available_skus())
            raise ValueError(
                f"Insufficient stock for sku={sku}. Available SKUs: {available}"
            )
        self._repo.decrease(sku, quantity)
