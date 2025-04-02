
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class PessoaCreate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    documento: Optional[str] = None
    nome: Optional[str] = None
    senha: str = Field(..., min_length=6)

class PessoaOut(BaseModel):
    id: str
    username: Optional[str]
    email: Optional[EmailStr]
    documento: Optional[str]
    nome: Optional[str]
    criado_em: datetime
