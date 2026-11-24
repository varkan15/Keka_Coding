import logging

from fastapi import APIRouter, status

from app.models import Item, ItemCreate
from app.repository import ItemRepository
from app.service import ItemService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/items", tags=["items"])

# Simple wiring: one shared in-memory repository for the app's lifetime.
_service = ItemService(ItemRepository())


@router.post("", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(request: ItemCreate) -> Item:
    logger.info("POST /api/items body=%s", request.model_dump())
    return _service.create_item(request)


@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    logger.info("GET /api/items/%s", item_id)
    return _service.get_item(item_id)
