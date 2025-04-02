
from fastapi import APIRouter, HTTPException, Depends
from datetime import date, timedelta
from app.models.turno import Shift, ShiftInDB
from app.db import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

router = APIRouter(prefix="/turnos", tags=["Turnos"])

@router.post("/", response_model=ShiftInDB)
async def criar_turno(shift: Shift, db: AsyncIOMotorDatabase = Depends(get_db)):
    existing = await db["turnos"].find_one({
        "user_id": shift.user_id,
        "day": shift.day.isoformat()
    })
    if existing:
        raise HTTPException(status_code=400, detail="Turno já existe para essa pessoa nesse dia.")
    result = await db["turnos"].insert_one(shift.dict(by_alias=True))
    shift_in_db = shift.dict()
    shift_in_db["_id"] = str(result.inserted_id)
    return shift_in_db

@router.get("/semana/{start_date}", response_model=List[ShiftInDB])
async def listar_turnos_da_semana(start_date: date, db: AsyncIOMotorDatabase = Depends(get_db)):
    end_date = start_date + timedelta(days=27)
    turnos = await db["turnos"].find({
        "day": {"$gte": start_date.isoformat(), "$lte": end_date.isoformat()}
    }).to_list(500)
    return turnos
