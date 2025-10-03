from pydantic import BaseModel
from typing import Optional,List

class GenreSchema(BaseModel):
    id: int
    genre: str

    class Config:
        orm_mode = True

from typing import Optional
from pydantic import BaseModel

class BookSchema(BaseModel):
    id: int
    title: Optional[str]
    genre_id: Optional[int]
    note: Optional[int]
    stock_number: Optional[int]
    datetime: Optional[str]
    upc: Optional[str]
    product_type: Optional[str]
    price_ht: Optional[float]
    price_taxed: Optional[float]
    review_number: Optional[int]
    description: Optional[str]

    class Config:
        orm_mode = True


