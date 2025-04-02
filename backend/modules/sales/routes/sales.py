from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from app.models.sale import Sale
from app.services.logic import (
    process_sale, update_sale_status, refund_sale,
    get_client_sales, get_sales_summary
)
from app.db import db

router = APIRouter()

@router.post("/sales")
async def create_sale(sale: Sale):
    try:
        sale_id = await process_sale(sale)
        return {"id": sale_id, "status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/sales")
async def list_sales(status: str = Query(None)):
    query = {"status": status} if status else {}
    sales = await db.sales.find(query).to_list(100)
    return sales

@router.get("/sales/summary")
async def summary(from_date: str, to_date: str):
    return await get_sales_summary(from_date, to_date)

@router.post("/sales/{sale_id}/status")
async def change_status(sale_id: str, status: str):
    try:
        await update_sale_status(sale_id, status)
        return {"id": sale_id, "status": status}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/sales/{sale_id}/refund")
async def refund(sale_id: str):
    try:
        await refund_sale(sale_id)
        return {"id": sale_id, "status": "cancelada"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/sales/client/{client_id}")
async def client_sales(client_id: str):
    return await get_client_sales(client_id)

@router.patch("/sales/{sale_id}/status")
async def update_status(sale_id: str, status: str):
    from bson import ObjectId
    valid_statuses = ["pendente", "pago", "cancelado", "entregue"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Status inválido")
    
    result = await db.sales.update_one(
        {"_id": ObjectId(sale_id)},
        {"$set": {"status": status}}
    )
    if result.modified_count:
        await add_sale_timeline(sale_id, f"Status alterado para {status}")
        if status == "entregue":
            await generate_delivery_link(sale_id)
        return {"status": "atualizado"}
    raise HTTPException(status_code=404, detail="Venda não encontrada")