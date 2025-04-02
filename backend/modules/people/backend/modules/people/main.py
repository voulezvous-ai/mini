
from fastapi import FastAPI
from app.routes import users
from app.core.database import connect_db

app = FastAPI(title="Módulo Pessoas")

@app.on_event("startup")
async def startup_db():
    await connect_db()

app.include_router(users.router, prefix="/pessoas", tags=["Pessoas"])
