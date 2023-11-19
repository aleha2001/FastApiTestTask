import logging
from datetime import datetime

from sqlalchemy.orm import Session
from .models import Text


def get_text(session: Session, text_id: int) -> Text:
    """
    Select Text row by id
    """
    logging.info(f"getting text {text_id=}")
    return session.query(Text).get(text_id)


def insert_text(session: Session, text_dict: dict) -> None:
    """
    Create new Text object
    """
    logging.info(f"inserting text {text_dict=}")
    new_text = Text(
        time_saved=datetime.strptime(
            text_dict.get("datetime"), "%d.%m.%Y %H:%M:%S.%f"
        ),
        title=text_dict.get("title"),
        text_len=text_dict.get("text_len"),
        x_count=text_dict.get("x_count"),
    )
    session.add(new_text)
    session.commit()
