from dataclasses import dataclass

from src.modules.order.internal.domain.order_item import OrderItem


@dataclass
class Order:
    order_id: str
    customer_id: str
    items: list[OrderItem]
    status: str
