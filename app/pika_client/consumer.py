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
        # connections_creds = pika.PlainCredentials(
        #     username=Config.rb_user, password=Config.rb_password
        # )
        # connections_params = pika.ConnectionParameters(
        #     Config.rb_host, credentials=connections_creds, port=Config.rb_port
        # )
        # self.connection = pika.BlockingConnection(connections_params)
        pass

    @staticmethod
    def process_text(message:IncomingMessage):
        """Counts x occurrences in text and saves to db"""
        body = message.body
        data = json.loads(body)
        print(f"message received {data}", type(data))
        data_text = data["text"]
        print(data_text)
        x_count = data_text.lower().count("x")
        print(f"data processed {x_count}")
        data.update({"x_count": x_count, "text_len": len(data_text)})
        insert_text(SessionLocal(), data)

    async def consume(self, loop):
        """Setup message listener with the current running loop"""
        connection = await aio_pika.connect_robust(
            host=Config.rb_host,
            port=Config.rb_port,
            login=Config.rb_user,
            password=Config.rb_password,
            loop=loop,
        )
        channel = await connection.channel()
        queue = await channel.declare_queue("texts")
        await queue.consume(self.process_text, no_ack=True)
        return connection

    async def close_connection(self):
        self.connection.close()


if __name__ == "__main__":
    pika_consumer = PikaConsumer()
    pika_consumer.consume()
