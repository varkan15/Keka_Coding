import logging

from app.exceptions import ConflictError, NotFoundError, ValidationError
from app.models import OrderResponse, OrderCreate, Order, Wallet
from app.repository import OrderRepository

logger = logging.getLogger(__name__)


class OrderService:
    """Business rules live here: no HTTP and no storage details."""

    def __init__(self, repository: OrderRepository) -> None:
        self._repo = repository

    def create_item(self, req: OrderCreate) -> OrderResponse:
        if not self._repo.emp_exists(req.emp_id):
            logger.warning("Item not found id=%s", req.emp_id)
            raise NotFoundError(f"Item {req.emp_id} not found")

        total = 0
        for item_id, qty in req.items:
            price = self._repo.itemPrice(item_id)
            total += price*qty

        with self._lock:
            if total > self._repo.getBalance(req.emp_id):
                logger.warning("Order out of budget")
                raise ValidationError("out of budget")

            self._repo.setBalance(emp_id, balance)
        

    def get_balance(self, emp_id: int) -> int:
        if not self._repo.emp_exists(emp_id):
            logger.warning("Item not found id=%s", emp_id)
            raise NotFoundError(f"Item {emp_id} not found")
        return self._repo.getBalance(emp_id)
