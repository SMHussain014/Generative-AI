from sqlmodel import SQLModel, Field
from typing import Optional, Union

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int | None = None
    user_id: int | None = None
    quantity: int | None = None
    amount: float = Field(min_length=3, max_length=8)
    status: str = "pending"

class OrderUpdate(SQLModel):
    quantity: int | None = None
    amount: float | None = None