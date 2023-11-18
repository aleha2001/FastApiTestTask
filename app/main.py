#!/usr/bin/env python3
import asyncio
import uvicorn
from fastapi import FastAPI
from db.database import engine
from db import models
from models import TextItem
from contextlib import asynccontextmanager
from consumer import PikaConsumer
from producer import PikaProducer


@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    loop = asyncio.get_running_loop()
    pika_consumer = PikaConsumer()
    task = loop.create_task(pika_consumer.consume(loop))
    pika_producer = PikaProducer()
    await task
    yield
    pika_producer.close_connection()


def create_app():
    app = FastAPI(docs_url="/", lifespan=lifespan)

    @app.post("/text")
    async def parse_text(text_item: TextItem):
        print(text_item)
        publish_text(text_item)
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
