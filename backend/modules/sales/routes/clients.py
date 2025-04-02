from fastapi import APIRouter, HTTPException, Query
from app.models.client import Client
from app.db import db

router = APIRouter()

@router.post("/clients")
async def create_client(client: Client):
    client_dict = client.dict()
    result = await db.clients.insert_one(client_dict)
    return {"id": str(result.inserted_id)}

@router.get("/clients")
async def list_clients(q: str = Query(None)):
    query = {"name": {"$regex": q, "$options": "i"}} if q else {}
    clients = await db.clients.find(query).to_list(100)
    return clients