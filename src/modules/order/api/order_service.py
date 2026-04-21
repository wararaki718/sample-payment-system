from decimal import Decimal
from uuid import uuid4

from src.modules.inventory.api.inventory_service import InventoryService
from src.modules.order.api.types import PlaceOrderRequest, PlaceOrderResult
from src.modules.order.events.order_placed import OrderPlaced
from src.modules.order.internal.domain.order import Order
from src.modules.order.internal.domain.order_item import OrderItem
from src.modules.order.internal.order_repository import OrderRepository
from src.modules.order.internal.order_validator import OrderValidator
from src.modules.payment.api.payment_service import PaymentService
from src.shared.event_bus import EventBus
from src.shared.types.money import Money


class OrderService:
    def __init__(
        self,
        inventory_service: InventoryService,
        payment_service: PaymentService,
        event_bus: EventBus,
    ) -> None:
        self._repository = OrderRepository()
        self._validator = OrderValidator()
        self._inventory_service = inventory_service
        self._payment_service = payment_service
        self._event_bus = event_bus

    def place_order(self, request: PlaceOrderRequest) -> PlaceOrderResult:
        self._validator.validate(request)

        order_items = [
            OrderItem(
                sku=item.sku,
                quantity=item.quantity,
                unit_price=Money(amount=item.unit_price, currency=request.currency.upper()),
            )
            for item in request.items
        ]

        for item in order_items:
            self._inventory_service.reserve(item.sku, item.quantity)

        total = sum((item.subtotal().amount for item in order_items), Decimal("0"))
        self._payment_service.charge(
            customer_id=request.customer_id,
            amount=Money(amount=total, currency=request.currency.upper()),
        )

        order = Order(
            order_id=str(uuid4()),
            customer_id=request.customer_id,
            items=order_items,
            status="PLACED",
        )
        self._repository.save(order)

        event = OrderPlaced(order_id=order.order_id, customer_id=order.customer_id, total=total)
        self._event_bus.publish(event)

        return PlaceOrderResult(order_id=order.order_id, status=order.status, charged=total)
