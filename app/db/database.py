import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from config.config import Config


# Config.db_host = "localhost"
# Config.db_user = "postgres"
# Config.db_name = "testbaum"
# Config.db_password = "aleha2001"


SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{Config.db_user}:{Config.db_password}@{Config.db_host}/{Config.db_name}"
)


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
