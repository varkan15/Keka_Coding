from pydantic import BaseModel, Field
from enum import Enum

class Status(str, Enum):
    PLACED = "PLACED"
    REJECTED = "REJECTED"

class Order(BaseModel):
    itemId: str
    qty: int

#Request Body
class OrderCreate(BaseModel):
    emp_id: str
    items: list[Order]

# Response body / stored entity.
class OrderResponse(BaseModel):
    order_id: int
    total: int
    walletBalance: int
    status: Status

#GET RESPONSE STRUCTURE
class Wallet(BaseModel):
    emp_id: str
    balance: int

class ErrorResponse(BaseModel):
    error: str
    message: str


