from fastapi import APIRouter, HTTPException
from fpdf import FPDF
from bson import ObjectId
import os
from datetime import datetime
from app.db import db

router = APIRouter()

@router.get("/sales/{sale_id}/receipt/pdf")
async def generate_pdf_receipt(sale_id: str):
    sale = await db.sales.find_one({"_id": ObjectId(sale_id)})
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    
    client = await db.clients.find_one({"_id": ObjectId(sale['client_id'])}) if 'client_id' in sale else None
    client_name = client.get("name") if client else "Cliente não identificado"
    client_phone = client.get("phone") if client else ""

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"RECIBO #{sale_id[:6]}", ln=True, align="R")

    pdf.set_font("Arial", size=11)
    pdf.cell(200, 10, txt=f"Cliente: {client_name}", ln=True)
    if client_phone:
        pdf.cell(200, 10, txt=f"Telefone: {client_phone}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Itens:", ln=True)

    pdf.set_font("Arial", size=11)
    for item in sale["products"]:
        name = item.get("product_name", "Sem nome")
        qty = item["quantity"]
        price = item["total_price"]
        pdf.cell(160, 8, txt=f"{qty}x {name}", ln=0)
        pdf.cell(30, 8, txt=f"{price:.2f} €", ln=1, align="R")

    pdf.ln(3)
    pdf.set_font("Arial", 'B', 13)
    pdf.cell(200, 10, txt=f"Total: {sale['total']:.2f} €", ln=1, align="R")

    pdf.set_font("Arial", size=10)
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    pdf.set_y(-30)
    pdf.cell(200, 8, txt=now, ln=1, align="C")
    pdf.cell(200, 8, txt="NIF: 123456789 | Empresa Exemplo Unipessoal LDA", ln=1, align="C")

    receipts_dir = "receipts"
    os.makedirs(receipts_dir, exist_ok=True)
    file_path = os.path.join(receipts_dir, f"sale_{sale_id}.pdf")
    pdf.output(file_path)

    return {"message": "Recibo gerado com sucesso", "path": file_path}