from app.db import db
from app.models.sale import Sale
from datetime import datetime
from bson import ObjectId
import uuid

async def process_sale(sale: Sale):
    # Verificar e atualizar estoque
    for item in sale.products:
        product = await db.products.find_one({"_id": ObjectId(item.product_id)})
        if not product or product["stock"] < item.quantity:
            raise ValueError(f"Estoque insuficiente para o produto {item.product_id}")
        await db.products.update_one(
            {"_id": ObjectId(item.product_id)},
            {"$inc": {"stock": -item.quantity}}
        )

    # Gerar link de entrega
    delivery_link = f"https://mini.app/delivery/{uuid.uuid4().hex}"

    # Criar venda
    sale_dict = sale.dict()
    sale_dict['payment_received'] = sale_dict.get('payment_received', sale_dict['total'])
    sale_dict['balance_due'] = sale_dict['total'] - sale_dict['payment_received'] - sale_dict.get('discount', 0)
    sale_dict["created_at"] = datetime.utcnow().isoformat()
    sale_dict["delivery_link"] = delivery_link
    sale_dict["timeline"] = [{"event": "Venda criada", "timestamp": datetime.utcnow().isoformat()}]
    result = await db.sales.insert_one(sale_dict)

    # Se pagamento for fiado, criar dívida em vez de débito
    if sale.payment_method == "fiado":
        await db.debts.insert_one({
            "person_id": sale.client_id,
            "amount": sale.total - sale.discount,
            "ref": str(result.inserted_id),
            "status": "aberta",
            "created_at": datetime.utcnow().isoformat()
        })
    else:
        await db.transactions.insert_one({
            "person_id": sale.client_id,
            "type": "debit",
            "amount": sale.total - sale.discount,
            "source": "venda",
            "ref_id": str(result.inserted_id),
            "created_at": datetime.utcnow().isoformat()
        })

    await update_client_risk_score(sale.client_id)
    sale_id = str(result.inserted_id)
    await add_sale_timeline(sale_id, 'Venda criada')
    return sale_id

async def update_sale_status(sale_id: str, new_status: str):
    sale = await db.sales.find_one({"_id": ObjectId(sale_id)})
    if not sale:
        raise ValueError("Venda não encontrada")
    await db.sales.update_one(
        {"_id": ObjectId(sale_id)},
        {
            "$set": {"status": new_status},
            "$push": {"timeline": {
                "event": f"Status atualizado para '{new_status}'",
                "timestamp": datetime.utcnow().isoformat()
            }}
        }
    )

async def refund_sale(sale_id: str):
    sale = await db.sales.find_one({"_id": ObjectId(sale_id)})
    if not sale:
        raise ValueError("Venda não encontrada")

    # Reembolso
    await db.transactions.insert_one({
        "person_id": sale["client_id"],
        "type": "credit",
        "amount": sale["total"] - sale.get("discount", 0),
        "source": "reembolso",
        "ref_id": sale_id,
        "created_at": datetime.utcnow().isoformat()
    })

    # Restaurar estoque
    for item in sale["products"]:
        await db.products.update_one(
            {"_id": ObjectId(item["product_id"])},
            {"$inc": {"stock": item["quantity"]}}
        )

    await update_sale_status(sale_id, "cancelada")

async def get_client_sales(client_id: str):
    sales = await db.sales.find({"client_id": client_id}).to_list(100)
    total = sum(sale["total"] - sale.get("discount", 0) for sale in sales)
    return {"client_id": client_id, "total_spent": total, "sales": sales}

async def get_sales_summary(start_date: str, end_date: str):
    from datetime import datetime
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)

    pipeline = [
        {
            "$match": {
                "created_at": {"$gte": start.isoformat(), "$lte": end.isoformat()}
            }
        },
        {
            "$group": {
                "_id": "$payment_method",
                "total": {"$sum": {"$subtract": ["$total", "$discount"]}},
                "count": {"$sum": 1}
            }
        }
    ]
    summary = await db.sales.aggregate(pipeline).to_list(None)
    return summary
from app.services.score import update_client_risk_score


async def add_sale_timeline(sale_id: str, event: str):
    from bson import ObjectId
    sale = await db.sales.find_one({"_id": ObjectId(sale_id)})
    if not sale:
        return
    timeline = sale.get("timeline", [])
    timeline.append({
        "timestamp": datetime.utcnow().isoformat(),
        "event": event
    })
    await db.sales.update_one(
        {"_id": ObjectId(sale_id)},
        {"$set": {"timeline": timeline}}
    )