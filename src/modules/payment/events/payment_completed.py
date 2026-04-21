from dataclasses import dataclass

from src.shared.types.money import Money


@dataclass(frozen=True)
class PaymentCompleted:
    customer_id: str
    amount: Money
    name: str = "payment.completed"
