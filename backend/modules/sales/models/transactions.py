from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Transaction(BaseModel):
    sale_id: Optional[str]
    client_id: Optional[str]
    method: str
    amount: float
    timestamp: datetime