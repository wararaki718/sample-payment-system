from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def __str__(self) -> str:
        return f"{self.amount} {self.currency}"
