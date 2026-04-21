from src.modules.order.internal.domain.order import Order


class OrderRepository:
    _store: dict[str, Order] = {}

    def save(self, order: Order) -> None:
        self._store[order.order_id] = order

    def find_by_id(self, order_id: str) -> Order | None:
        return self._store.get(order_id)
