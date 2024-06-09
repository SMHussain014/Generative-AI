from sqlmodel import SQLModel, Field
from typing import Optional, Union

class Order(SQLModel):
    id: Optional[int] = Field(default=None)
    username: str
    product_id: int
    product_name: str
    price: int
