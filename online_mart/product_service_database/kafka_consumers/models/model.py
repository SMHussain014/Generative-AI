from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, Union

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=5, max_length=30)
    description: str
    price: float = Field(min_length=3, max_length=8)
    category: str
    brand: str | None = None
    color: str | None = None
    weight: float | None = None
    stock: int | None = None
    sku: str | None = None
    # rating: list["ProductRating"] = Relationship(back_populates="product")
    # image: str # Multiple | URL Not Media | One to Manu Relationship
    # rating: float | None = None # One to Manu Relationship

# class ProductRating(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     product_id: int = Field(foreign_key="product.id")
#     rating: int
#     review: str | None = None
#     product = Relationship(back_populates="rating")
#     user_id: int # One to Manu Relationship

class ProductUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    category: str | None = None
    brand: str | None = None
    color: str | None = None
    weight: float | None = None
    stock: int | None = None
    sku: str | None = None
