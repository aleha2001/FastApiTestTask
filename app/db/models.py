from sqlalchemy import DateTime, Column, ForeignKey, Integer, String, func
from .database import Base


class Text(Base):
    __tablename__ = "texts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    time_saved = Column(DateTime(timezone=True), server_default=func.now())
    title = Column(String, index=True)
    text_len = Column(Integer, server_default="0")
    x_count = Column(Integer, server_default="0")
