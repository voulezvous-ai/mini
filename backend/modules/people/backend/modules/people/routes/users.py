
from fastapi import APIRouter, HTTPException
from app.schemas.user import PessoaCreate, PessoaOut
from app.services.users import criar_pessoa

router = APIRouter()

@router.post("/", response_model=PessoaOut)
async def registrar_pessoa(pessoa: PessoaCreate):
    return await criar_pessoa(pessoa)
