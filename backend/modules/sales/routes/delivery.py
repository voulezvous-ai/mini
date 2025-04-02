from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.db import db

router = APIRouter()

@router.get("/delivery/{sale_id}")
async def get_delivery_info(sale_id: str):
    sale = await db.sales.find_one({"_id": ObjectId(sale_id)})
    if not sale or "delivery" not in sale:
        raise HTTPException(status_code=404, detail="Entrega não encontrada")
    return sale["delivery"]