
from app.core.database import db
from app.schemas.user import PessoaCreate, PessoaOut
from datetime import datetime
from bson import ObjectId
import hashlib

def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

async def criar_pessoa(pessoa: PessoaCreate):
    dados = pessoa.dict()
    dados["senha"] = hash_senha(dados["senha"])
    dados["criado_em"] = datetime.utcnow()
    result = await db.pessoas.insert_one(dados)
    return PessoaOut(id=str(result.inserted_id), **{k: dados[k] for k in ["username", "email", "documento", "nome", "criado_em"]})
