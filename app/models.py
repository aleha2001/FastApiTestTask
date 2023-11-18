from pydantic import BaseModel
from datetime import datetime


class TextItem(BaseModel):
    datetime: datetime
    title: str
    text: str


class TextDbItem(BaseModel):
    datetime: datetime
    title: str
    x_avg: float
