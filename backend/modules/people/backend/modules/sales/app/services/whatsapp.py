import os
from bson import ObjectId
from app.db import db
from datetime import datetime

async def send_whatsapp_receipt(sale_id: str):
    sale = await db.sales.find_one({"_id": ObjectId(sale_id)})
    if not sale:
        print(f"[WhatsApp] Venda {sale_id} não encontrada.")
        return

    client = await db.clients.find_one({"_id": ObjectId(sale['client_id'])}) if 'client_id' in sale else None
    if not client or not client.get("phone"):
        print(f"[WhatsApp] Cliente sem telefone. Não foi possível enviar o recibo.")
        return

    phone = client["phone"]
    file_path = f"receipts/sale_{sale_id}.pdf"

    if not os.path.exists(file_path):
        print(f"[WhatsApp] Recibo não encontrado. Gerando novo...")
        from app.routes.receipt_pdf import generate_pdf_receipt
        await generate_pdf_receipt(sale_id)

    print(f"[WhatsApp] Enviando recibo da venda {sale_id} para {phone}...")
    print(f"[WhatsApp] Arquivo: {file_path}")
    print(f"[WhatsApp] Mensagem enviada às {datetime.now().strftime('%H:%M:%S')} (simulação)")