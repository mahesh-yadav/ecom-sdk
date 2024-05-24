from pydantic import BaseModel


class Store(BaseModel):
    id: int
    name: str
    products: int


class Product(BaseModel):
    id: int
    name: str
    price: float