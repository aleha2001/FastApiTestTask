#!/usr/bin/env python3
import asyncio

import uvicorn
from fastapi import FastAPI

from db.database import engine
from db import models
from models import TextItem
import pika


def create_app():
    app = FastAPI(docs_url="/")


    @app.on_event("startup")
    async def startup_event():
        # models.Base.metadata.create_all(bind=engine)
        pass

    @app.post("/text")
    async def parse_text(text_item: TextItem):
        print(text_item)
        asyncio.create_task(publish_text(text_item))
        return text_item

    return app


def main():
    uvicorn.run(
        f"{__name__}:create_app",
        host="0.0.0.0",
        port=8888,
    )


if __name__ == "__main__":
    main()
