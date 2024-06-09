from sqlmodel import SQLModel, Field
from typing import Optional, Union

# Create Model for Products
class Products(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_category: str
    product_name: str = Field(index=True, min_length=5, max_length=30)
    size: str
    price: int = Field(min_length=3, max_length=8)