from bson import ObjectId
from app.db import db

async def update_client_risk_score(client_id: str):
    sales = await db.sales.find({"client_id": client_id}).to_list(100)
    if not sales:
        score = 0.0
    else:
        total_due = sum(s.get("balance_due", 0) for s in sales)
        total_paid = sum(s.get("payment_received", 0) for s in sales)
        score = 1.0 - (total_due / (total_paid + total_due)) if (total_paid + total_due) > 0 else 1.0
        score = round(score * 100, 2)

    await db.clients.update_one({"_id": ObjectId(client_id)}, {"$set": {"risk_score": score}})