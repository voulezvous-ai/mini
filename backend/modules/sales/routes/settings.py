from fastapi import APIRouter
from app.db import db
from app.models.settings import Settings

router = APIRouter()

@router.get("/settings")
async def get_settings():
    doc = await db.settings.find_one({})
    if not doc:
        default = Settings().dict()
        await db.settings.insert_one(default)
        return default
    return doc

@router.put("/settings")
async def update_settings(new_settings: Settings):
    await db.settings.update_one({}, {"$set": new_settings.dict()}, upsert=True)
    return {"status": "updated"}