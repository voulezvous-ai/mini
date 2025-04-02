
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import IndexModel, ASCENDING
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = None
db = None

async def connect_db():
    global client, db
    client = AsyncIOMotorClient(MONGO_URL)
    db = client["mini"]

    # Índices para garantir unicidade
    await db.pessoas.create_indexes([
        IndexModel([("email", ASCENDING)], unique=True, sparse=True),
        IndexModel([("username", ASCENDING)], unique=True, sparse=True),
        IndexModel([("documento", ASCENDING)], unique=True, sparse=True)
    ])
