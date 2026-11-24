import logging

from app.exceptions import ConflictError, NotFoundError, ValidationError
from app.models import Item, ItemCreate
from app.repository import ItemRepository

logger = logging.getLogger(__name__)


class ItemService:
    """Business rules live here: no HTTP and no storage details."""

    def __init__(self, repository: ItemRepository) -> None:
        self._repo = repository

    def create_item(self, request: ItemCreate) -> Item:
        name = request.name.strip()
        if not name:
            raise ValidationError("name must not be blank")
        if self._repo.find_by_name(name):
            logger.warning("Rejected duplicate item name=%s", name)
            raise ConflictError(f"Item with name '{name}' already exists")

        item = self._repo.save(name, request.quantity, request.price)
        logger.info("Created item id=%s name=%s", item.id, item.name)
        return item

    def get_item(self, item_id: int) -> Item:
        item = self._repo.find_by_id(item_id)
        if item is None:
            logger.warning("Item not found id=%s", item_id)
            raise NotFoundError(f"Item {item_id} not found")
        return item
