from pydantic import BaseModel, Field


# Request body: Pydantic parses and validates the JSON for us.
class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    quantity: int = Field(ge=0)
    price: float = Field(gt=0)


# Response body / stored entity.
class Item(BaseModel):
    id: int
    name: str
    quantity: int
    price: float


class ErrorResponse(BaseModel):
    error: str
    message: str
