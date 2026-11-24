import logging
from threading import Lock

from app.models import Item

logger = logging.getLogger(__name__)


class ItemRepository:
    """In-memory storage. Only this class knows how data is kept."""

    def __init__(self) -> None:
        self._items: dict[int, Item] = {}
        self._next_id = 1
        self._lock = Lock()

    def save(self, name: str, quantity: int, price: float) -> Item:
        with self._lock:
            item = Item(id=self._next_id, name=name, quantity=quantity, price=price)
            self._items[item.id] = item
            self._next_id += 1
        logger.debug("Saved item %s", item)
        return item

    def find_by_id(self, item_id: int) -> Item | None:
        return self._items.get(item_id)

    def find_by_name(self, name: str) -> Item | None:
        return next(
            (i for i in self._items.values() if i.name.lower() == name.lower()), None
        )

    def find_all(self) -> list[Item]:
        return list(self._items.values())
