import json
import pika
import asyncio
from models import TextItem
from datetime import datetime
from config.config import Config


class PikaProducer:
    def __init__(self):
        connections_params = pika.ConnectionParameters(Config.rb_host)
        self.connection = pika.BlockingConnection(connections_params)
        self.chanel = self.connection.channel()

    def publish_text(self, text_item: TextItem):
        text_item_json = json.dumps(
            text_item.model_dump(), indent=4, sort_keys=True, default=str
        )

        self.chanel.queue_declare(queue="texts")
        self.chanel.basic_publish(exchange="", routing_key="texts", body=text_item_json)
        print(f"sent text: {text_item}")

    def close_connection(self):
        self.connection.close()


if __name__ == "__main__":
    text_item_data = {"datetime": datetime.now(), "title": "text1", "text": "text1"}
    pika_producer = PikaProducer()
    pika_producer.publish_text(TextItem(**text_item_data))
