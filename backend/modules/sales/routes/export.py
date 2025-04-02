from fastapi import APIRouter
from app.db import db
import json, os
from datetime import datetime
from zipfile import ZipFile

router = APIRouter()

@router.get("/export")
async def export_data():
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    folder = f"export_{timestamp}"
    os.makedirs(folder, exist_ok=True)

    collections = ["products", "clients", "sales", "settings"]
    for col in collections:
        data = await db[col].find().to_list(length=None)
        with open(f"{folder}/{col}.json", "w") as f:
            json.dump(data, f, indent=2, default=str)

    zip_path = f"{folder}.zip"
    with ZipFile(zip_path, "w") as zipf:
        for file in os.listdir(folder):
            zipf.write(os.path.join(folder, file), arcname=file)

    return {"status": "ok", "path": zip_path}