from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import view
from app.ws.websocket import websocket_endpoint

app = FastAPI()
app.include_router(view.router)
app.add_api_websocket_route("/ws/delivery/{uuid}", websocket_endpoint)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")