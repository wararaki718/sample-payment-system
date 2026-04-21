from dataclasses import dataclass

from src.shared.types.money import Money


@dataclass
class OrderItem:
    sku: str
    quantity: int
    unit_price: Money

    def subtotal(self) -> Money:
        return Money(amount=self.unit_price.amount * self.quantity, currency=self.unit_price.currency)
