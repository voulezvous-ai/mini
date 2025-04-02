
from pydantic import BaseModel, Field
from datetime import datetime, time
from typing import Optional

class CheckIn(BaseModel):
    user_id: str
    name: str
    role: str
    shift_start: time
    checkin_time: datetime
    is_late: bool

class CheckInInDB(CheckIn):
    id: Optional[str] = Field(alias="_id")
