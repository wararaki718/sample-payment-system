from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class OrderPlaced:
    order_id: str
    customer_id: str
    total: Decimal
    name: str = "order.placed"
