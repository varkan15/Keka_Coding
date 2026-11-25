import logging
from threading import Lock
from models import Order, OrderResponse

from app.models import Item

logger = logging.getLogger(__name__)


class OrderRepository:
    """In-memory storage. Only this class knows how data is kept."""

    def __init__(self) -> None:
        self._menu = { "itm-1": {"name": "Masala Dosa", "price": 60},
                      "itm-2": {"name": "Filter Coffee", "price": 25},
                      "itm-3": {"name": "Samosa", "price": 15}}
         
        self._orders = dict[int, OrderResponse] = {}
        self._wallets = {"emp-101": 500, "emp-102" : 100}
        self._next_id = 1
        self._lock = Lock()

    def emp_exists(self, emp_id):
        return emp_id in self._wallets

    def itemPrice(self, item_id):
        return self._menu[item_id]["price"]
    
    def save(self, total, walletBalance, status) -> OrderResponse:
        with self._lock:
            order_res = OrderResponse(self._next_id, total, walletBalance, status)
            self._orders[self._next_id] = order_res
            self._next_id += 1
        logger.debug("Saved item %s", order_res)
        return order_res

    def getBalance(self, emp_id):
        return self._wallets[emp_id]

    def setBalance(self, emp_id, val):
        self._wallets[emp_id] = val
