from fastapi import FastAPI
from app.routes import settings, analytics, export, delivery, products, sales, clients, receipt, receipt_pdf

app = FastAPI(title="Sales Mini")

app.include_router(products.router, tags=["Products"])
app.include_router(delivery.router, tags=["Delivery"])
app.include_router(settings.router, tags=["Settings"])
app.include_router(analytics.router, tags=["Analytics"])
app.include_router(export.router, tags=["Export"])
app.include_router(sales.router, tags=["Sales"])
app.include_router(clients.router, tags=["Clients"])
app.include_router(receipt.router, tags=["Receipt"])
app.include_router(receipt_pdf.router, tags=["PDF Receipt"])