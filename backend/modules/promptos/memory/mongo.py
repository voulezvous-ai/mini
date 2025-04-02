from motor.motor_asyncio import AsyncIOMotorClient
import os
from memory.logger import logger

MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    logger.warning("MONGODB_URI não definida. Conexão com MongoDB não será estabelecida.")

client = AsyncIOMotorClient(MONGODB_URI) if MONGODB_URI else None
db = client.agentos if client else None

async def log_action(prompt, result):
    if db:
        try:
            await db.prompt_logs.insert_one({
                "prompt": prompt,
                "result": result,
                "status": result.get("status", "executed")
            })
        except Exception as e:
            logger.exception("Erro ao registrar ação no MongoDB.")
    else:
        logger.info("MongoDB não configurado. Log não salvo.")