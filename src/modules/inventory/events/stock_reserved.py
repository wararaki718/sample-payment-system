from dataclasses import dataclass


@dataclass(frozen=True)
class StockReserved:
    sku: str
    quantity: int
    name: str = "inventory.stock_reserved"
