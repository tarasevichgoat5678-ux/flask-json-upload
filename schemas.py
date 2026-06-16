from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class JsonItem(BaseModel):
    name: str = Field(..., min_length=1, max_length=49)
    date: datetime

    @field_validator("date", mode="before")
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, datetime):
            return value
        return datetime.strptime(str(value), "%Y-%m-%d_%H:%M")
