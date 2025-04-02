from enum import Enum
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List



class PaymentEntry(BaseModel):
    method: str
    amount: float
    timestamp: Optional[str]

class SaleStatus(str, Enum):
    pending = "pendente"
    paid = "pago"
    cancelled = "cancelado"
    delivered = "entregue"

class SaleProduct(BaseModel):
    product_id: str
    quantity: int




    method: str
    amount: float
    timestamp: Optional[str]

    pending = "pendente"
    paid = "pago"
    cancelled = "cancelado"
    delivered = "entregue"

class SaleProduct(BaseModel):
    product_id: str
    product_name: Optional[str]
    unit_price: float = Field(..., ge=0)
    quantity: int = Field(..., gt=0)
    total_price: float

class Sale(BaseModel):
    id: Optional[str]
    client_id: str
    products: List[SaleProduct]
    total: float
    payment_method: str  # dinheiro, cartao, pix, fiado
    discount: Optional[float] = 0.0
    notes: Optional[str] = None
    status: str = "pendente"
    delivery_person: Optional[str] = None
    created_at: datetime

    payment_received: Optional[float] = None
    balance_due: Optional[float] = None

    @validator('total')
    def validate_total(cls, v, values):
        products = values.get('products', [])
        expected = round(sum(p['total_price'] for p in products), 2)
        if round(v, 2) != expected:
            raise ValueError(f'Total ({v}) não bate com soma dos produtos ({expected})')
        return v

from typing import List

class TimelineEvent(BaseModel):
    timestamp: str
    event: str

    class Config:
        extra = "ignore"

Sale.update_forward_refs()
Sale.__annotations__['timeline'] = Optional[List[TimelineEvent]]
Sale.__annotations__['payments'] = Optional[List[PaymentEntry]]