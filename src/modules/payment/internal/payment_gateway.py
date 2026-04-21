from src.shared.types.money import Money


class PaymentGateway:
    def charge(self, customer_id: str, amount: Money) -> None:
        # Simulate gateway side validation.
        if customer_id.startswith("blocked-"):
            raise ValueError("Payment rejected for this customer")
