from pydantic import BaseModel, Field
from typing import Optional

class Client(BaseModel):
    id: Optional[str]
    name: str
    phone: Optional[str] = Field(default=None, pattern=r'^\+?[0-9]{9,15}$')
    email: Optional[str]
    risk_score: Optional[float] = 0.0  # calculado com base em histórico
    notes: Optional[str] = None