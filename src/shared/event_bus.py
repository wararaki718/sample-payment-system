from typing import Protocol


class Event(Protocol):
    name: str


class EventBus:
    def __init__(self) -> None:
        self.events: list[Event] = []

    def publish(self, event: Event) -> None:
        self.events.append(event)
