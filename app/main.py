#!/usr/bin/env python3
import asyncio
import logging
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from db.database import SessionLocal, engine
from db import models
from db.queries import get_text
from models import TextItem, TextDbItem
from pika_client.consumer import PikaConsumer
from pika_client.producer import PikaProducer


def create_app():
    app = FastAPI(docs_url="/")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

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
        request.app.state.pika_producer.publish_text(text_item)
        return text_item

    @app.get("/text/{text_id}", response_model=TextDbItem)
    async def get_text_by_id(text_id: int):
        db_text = get_text(SessionLocal(), text_id=text_id)
        if db_text is None:
            logging.warning("no text found")
            raise HTTPException(status_code=404, detail="Item not found")
        item = TextDbItem(
            datetime=db_text.time_saved,
            title=db_text.title,
            x_avg=round(db_text.x_count / db_text.text_len, 3),
        )

        return item

    return app


def main():
    uvicorn.run(
        f"{__name__}:create_app",
        host="0.0.0.0",
        port=8888,
    )


if __name__ == "__main__":
    main()
