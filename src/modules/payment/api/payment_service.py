from src.modules.payment.internal.payment_gateway import PaymentGateway
from src.shared.types.money import Money


class PaymentService:
    def __init__(self) -> None:
        self._gateway = PaymentGateway()

    def charge(self, customer_id: str, amount: Money) -> None:
        if amount.amount <= 0:
            raise ValueError("Charge amount must be positive")
        self._gateway.charge(customer_id=customer_id, amount=amount)
