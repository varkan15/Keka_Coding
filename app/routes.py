import logging

from fastapi import APIRouter, status

from app.models import Wallet, OrderRequest, OrderResponse
from app.repository import OrderRepository
from app.service import OrderService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["items"])

# Simple wiring: one shared in-memory repository for the app's lifetime.
_service = OrderService(OrderRepository())


@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_item(request: OrderRequest) -> OrderResponse:
    logger.info("POST /api/items body=%s", request.model_dump())
    return _service.create_item(request)


@router.get("/{emp_id}", response_model=Wallet)
def get_item(emp_id: int) -> Wallet:
    logger.info("GET /api/items/%s", emp_id)
    return Wallet(emp_id, _service.get_balance(emp_id))
