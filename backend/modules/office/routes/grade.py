
from fastapi import APIRouter, Depends
from app.db import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import date, timedelta

router = APIRouter(prefix="/grade", tags=["Grade Consolidada"])

@router.get("/semana")
async def grade_consolidada(db: AsyncIOMotorDatabase = Depends(get_db)):
    hoje = date.today()
    semana = [hoje + timedelta(days=i) for i in range(0, 28)]  # 4 semanas

    # Coletar todos os turnos nesse intervalo
    turnos = await db["turnos"].find({
        "day": {"$in": [d.isoformat() for d in semana]}
    }).to_list(None)

    # Coletar todos os check-ins
    checkins = await db["checkins"].find({
        "checkin_time": {
            "$gte": f"{semana[0].isoformat()}T00:00:00",
            "$lte": f"{semana[-1].isoformat()}T23:59:59"
        }
    }).to_list(None)

    pessoas = set([t["name"] for t in turnos])
    grade = {}

    for pessoa in pessoas:
        grade[pessoa] = []
        for dia in semana:
            dia_str = dia.isoformat()
            turno = next((t for t in turnos if t["name"] == pessoa and t["day"] == dia_str), None)
            if not turno:
                grade[pessoa].append("vazio")
                continue
            if not turno.get("liberado"):
                grade[pessoa].append("previsto")
                continue
            checkin = next((c for c in checkins if c["name"] == pessoa and c["checkin_time"].startswith(dia_str)), None)
            if not checkin:
                grade[pessoa].append("falta")
            elif checkin.get("is_late"):
                grade[pessoa].append("atraso")
            else:
                grade[pessoa].append("presente")

    return {
        "dias": [d.isoformat() for d in semana],
        "grade": grade
    }
