from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from bson import ObjectId
from app.db import db

router = APIRouter()

@router.get("/sales/{sale_id}/receipt")
async def get_receipt(sale_id: str):
    sale = await db.sales.find_one({"_id": ObjectId(sale_id)})
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    
    client = await db.clients.find_one({"_id": ObjectId(sale['client_id'])}) if 'client_id' in sale else None
    receipt = {
        "cliente": client.get("name") if client else "Não informado",
        "produtos": sale["products"],
        "total": sale["total"],
        "desconto": sale.get("discount", 0),
        "recebido": sale.get("payment_received", 0),
        "saldo_restante": sale.get("balance_due", 0),
        "forma_pagamento": sale.get("payment_method"),
        "status": sale.get("status"),
        "entregador": sale.get("delivery_person"),
        "timeline": sale.get("timeline", [])
    }
    return JSONResponse(content=receipt)