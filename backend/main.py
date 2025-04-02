
from fastapi import FastAPI, Request
from backend.modules.promptos.interface import cli
from backend.modules.sales.routes import sales, products, clients, receipt, receipt_pdf, delivery as sales_delivery, export, analytics, settings
from backend.modules.office.routes import turnos
from backend.modules.delivery.routes import entregas

app = FastAPI(title="Mini Suite - Backup Rebuild")

# Sales
app.include_router(sales.router, tags=["Sales"])
app.include_router(products.router, tags=["Products"])
app.include_router(clients.router, tags=["Clients"])
app.include_router(receipt.router, tags=["Receipt"])
app.include_router(receipt_pdf.router, tags=["PDF Receipt"])
app.include_router(sales_delivery.router, tags=["Sales Delivery"])
app.include_router(export.router, tags=["Export"])
app.include_router(analytics.router, tags=["Analytics"])
app.include_router(settings.router, tags=["Settings"])

# Office
app.include_router(turnos.router, prefix="/office", tags=["Office"])

# Delivery
app.include_router(entregas.router, prefix="/delivery", tags=["Delivery"])

# PromptOS (CLI Interface Simulada)
@app.post("/prompt")
async def prompt_handler(request: Request):
    data = await request.json()
    return await cli.handle(data)
