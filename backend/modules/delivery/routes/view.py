from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/delivery/view/{uuid}")
def delivery_page(uuid: str, request: Request):
    return templates.TemplateResponse("delivery.html", {"request": request, "uuid": uuid})