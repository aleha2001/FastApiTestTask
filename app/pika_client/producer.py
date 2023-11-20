import json
from datetime import datetime

import aio_pika

from config.config import Config
from models import TextItem


class PikaProducer:
    """
    Pika Producer class
    """

    def __init__(self):
        self.connection = None

    async def publish_text(self, text_item: TextItem, loop):
        """
        Sends text to rabbitmq
        """

        text_item_json = json.dumps(
            text_item.model_dump(), indent=4, sort_keys=True, default=str
        )

        self.connection = await aio_pika.connect_robust(
            host=Config.rb_host,
            port=Config.rb_port,
            login=Config.rb_user,
            password=Config.rb_password,
            loop=loop,
        )

        chanel = await self.connection.channel()
        await chanel.declare_queue("texts")
        await chanel.default_exchange.publish(
            aio_pika.Message(
                body=text_item_json.encode("utf-8"),
                content_type="application/json",
                delivery_mode=2,  # Persistent message
            ),
            routing_key="texts",
        )

    async def close_connection(self):
        await self.connection.close()


if __name__ == "__main__":
    text_item_data = {"datetime": datetime.now(), "title": "text1", "text": "text1"}
    pika_producer = PikaProducer()
    pika_producer.publish_text(TextItem(**text_item_data))
