from sqlalchemy.orm import Session
from .models import Text


def get_text(session: Session, text_id: int):
    """
    Select Text row by id
    """
    print("Getting text from db")
    return session.query(Text).get(text_id)


def insert_text(session: Session, text_dict):
    """
    Create new Text object
    """
    print("Inserting text in db")
    new_text = Text(
        time_saved=text_dict.get("time_saved"),
        title=text_dict.get("title"),
        text_len=text_dict.get("text_len"),
        x_count=text_dict.get("x_count"),
    )
    session.add(new_text)
    session.commit()
