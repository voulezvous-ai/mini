
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time
from bson import ObjectId

class Shift(BaseModel):
    user_id: str
    name: str
    role: str
    day: date
    start_time: time
    end_time: time
    assigned_by: Optional[str] = None  # chefe de turno
    confirmed: bool = False            # check manual ou automático

class ShiftInDB(Shift):
    id: Optional[str] = Field(alias="_id")
