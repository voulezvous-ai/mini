from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.models.product import Product
from app.db import db

router = APIRouter()

@router.post("/products")
async def create_product(product: Product):
    product_dict = product.dict()
    result = await db.products.insert_one(product_dict)
    return {"id": str(result.inserted_id)}

@router.get("/products")
async def list_products():
    products = await db.products.find({"active": True}).to_list(100)
    return products

@router.put("/products/{product_id}")
async def update_product(product_id: str, product: Product):
    result = await db.products.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": product.dict(exclude_unset=True)}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"status": "updated"}

@router.delete("/products/{product_id}")
async def deactivate_product(product_id: str):
    result = await db.products.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": {"active": False}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"status": "deactivated"}

@router.get("/products/low-stock")
async def low_stock():
    products = await db.products.find({
        "active": True,
        "$expr": {"$lt": ["$stock", "$min_stock"]}
    }).to_list(100)
    return products