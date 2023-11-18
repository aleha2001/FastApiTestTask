#!/usr/bin/env python3
import asyncio

import pika
import uvicorn
from fastapi import FastAPI, Request

from config.config import Config
from db.database import engine
from db import models
from models import TextItem
from contextlib import asynccontextmanager
from pika_client.consumer import PikaConsumer
from pika_client.producer import PikaProducer


def test():
    print("test connection")
    # print(f"{Config.rb_user=},{Config.rb_host=},{Config.rb_password=},{Config.rb_port=}")


def create_app():
    app = FastAPI(docs_url="/")

    @app.on_event("startup")
    async def startapp():
        models.Base.metadata.create_all(bind=engine)
        pika_consumer = PikaConsumer()
        pika_producer = PikaProducer()
        app.state.pika_producer = pika_producer
        app.state.pika_consumer = pika_consumer
        loop = asyncio.get_running_loop()
        task = loop.create_task(pika_consumer.consume(loop))
        await task

    @app.post("/text")
    async def parse_text(request: Request, text_item: TextItem):
        print(text_item)
        request.app.state.pika_producer.publish_text(text_item)
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
