from pydantic import BaseModel
from typing import Optional, List

class Settings(BaseModel):
    payment_methods_enabled: Optional[List[str]] = ["dinheiro", "pix", "cartao"]
    allow_credit_sales: bool = True
    default_discount_percent: float = 0.0
    business_name: Optional[str] = "Minha Loja"
    business_nif: Optional[str] = "123456789"
    business_address: Optional[str] = "Rua Exemplo, 123"