from pydantic import BaseModel
from datetime import datetime


class TextItem(BaseModel):
    datetime: str
    title: str
    text: str


class TextDbItem(BaseModel):
    datetime: str
    title: str
    x_avg: float
