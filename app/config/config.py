import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv(".env")
db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
rb_port = os.getenv("RB_PORT")
rb_user = os.getenv("RB_USER")
rb_password = os.getenv("RB_PASSWORD")
rb_host = os.getenv("RB_HOST")


@dataclass
class Config:
    db_port: int = db_port
    db_user: str = db_user
    db_password: str = db_password
    db_host: str = db_host
    db_name: str = db_name
    rb_port: int = rb_port
    rb_user: str = rb_user
    rb_password: str = rb_password
    rb_host: str = rb_host

