from fastapi import APIRouter
from datetime import datetime, timedelta
from app.db import db

router = APIRouter()

@router.get("/sales/analytics")
async def sales_analytics(days: int = 7):
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    pipeline = [
        {"$match": {
            "created_at": {"$gte": start_date, "$lte": end_date}
        }},
        {"$project": {
            "day": {"$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}},
            "total": 1,
            "payments": 1
        }},
        {"$group": {
            "_id": "$day",
            "total_vendas": {"$sum": 1},
            "faturamento": {"$sum": "$total"},
            "media": {"$avg": "$total"}
        }},
        {"$sort": {"_id": 1}}
    ]
    summary = await db.sales.aggregate(pipeline).to_list(length=None)
    return summary