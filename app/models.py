from pydantic import BaseModel
from datetime import datetime


class TextItem(BaseModel):
    datetime: datetime
    title: str
    text: str
