from src.modules.order.api.types import PlaceOrderRequest


class OrderValidator:
    def validate(self, request: PlaceOrderRequest) -> None:
        if len(request.currency) != 3:
            raise ValueError("Currency must be a 3-letter ISO code")
