from pydantic import BaseModel, Field
from typing import Optional

class Product(BaseModel):
    id: Optional[str]
    name: str
    price: float = Field(..., ge=0)
    unit: Optional[str] = "unid"
    active: bool = True
    category: Optional[str] = None
    min_stock: Optional[int] = 0