from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Debt(BaseModel):
    client_id: str
    sale_id: str
    value: float
    status: Optional[str] = "pendente"
    created_at: datetime