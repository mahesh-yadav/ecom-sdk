from pydantic import BaseModel


class EcomAPIConfig(BaseModel):
    api_url: str
    api_key: str


class Store(BaseModel):
    id: int
    name: str
    products: int


class Product(BaseModel):
    id: int
    name: str
    price: float
