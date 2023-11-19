import logging

import pika
import aio_pika
from aio_pika import IncomingMessage
import asyncio
import json
from db.database import SessionLocal
from db.queries import insert_text, get_text
from config.config import Config


class PikaConsumer:
    """PikaConsumer class"""

    def __init__(self):
        self.connection = None

    @staticmethod
    async def process_text(message: IncomingMessage):
        """Counts x occurrences in text and saves to db"""
        body = message.body
        data = json.loads(body)
        logging.info(f"{data=}")
        data_text = data["text"]
        x_count = data_text.lower().count("х")
        logging.info(f"data processed,{x_count=}")
        data.update({"x_count": x_count, "text_len": len(data_text)})
        insert_text(SessionLocal(), data)

    async def consume(self, loop):
        """Setup message listener with the current running loop"""
        self.connection = await aio_pika.connect_robust(
            host=Config.rb_host,
            port=Config.rb_port,
            login=Config.rb_user,
            password=Config.rb_password,
            loop=loop,
        )
        channel = await self.connection.channel()
        queue = await channel.declare_queue("texts")
        await queue.consume(self.process_text, no_ack=False)

    async def close_connection(self):
        await self.connection.close()


if __name__ == "__main__":
    pika_consumer = PikaConsumer()
    pika_consumer.consume()
