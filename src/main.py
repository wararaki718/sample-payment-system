from fastapi import FastAPI, HTTPException

from src.modules.order.api.order_service import OrderService
from src.modules.order.api.types import PlaceOrderRequest
from src.modules.inventory.api.inventory_service import InventoryService
from src.modules.payment.api.payment_service import PaymentService
from src.shared.event_bus import EventBus


app = FastAPI(title="Sample Payment System")

event_bus = EventBus()
inventory_service = InventoryService()
payment_service = PaymentService()
order_service = OrderService(
    inventory_service=inventory_service,
    payment_service=payment_service,
    event_bus=event_bus,
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/orders")
def place_order(payload: PlaceOrderRequest) -> dict:
    try:
        result = order_service.place_order(payload)
        return {
            "order_id": result.order_id,
            "status": result.status,
            "charged": str(result.charged),
            "events": [event.name for event in event_bus.events],
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
