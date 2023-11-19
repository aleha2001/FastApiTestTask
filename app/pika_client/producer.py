import json
import logging

import pika
import asyncio
from models import TextItem
from datetime import datetime
from config.config import Config


class PikaProducer:
    """
    Pika Producer class
    """

    def __init__(self):
        connections_creds = pika.PlainCredentials(
            username=Config.rb_user, password=Config.rb_password
        )
        self.connections_params = pika.ConnectionParameters(
            Config.rb_host, credentials=connections_creds, port=Config.rb_port
        )
        self.connection = pika.BlockingConnection(self.connections_params)

    def publish_text(self, text_item: TextItem):
        """
        Sends text to rabbitmq
        """
        chanel = self.connection.channel()
        chanel.queue_declare(queue="texts")
        text_item_json = json.dumps(
            text_item.model_dump(), indent=4, sort_keys=True, default=str
        )

        chanel.queue_declare(queue="texts")
        chanel.basic_publish(exchange="", routing_key="texts", body=text_item_json)
        logging.info(f"sent text: {text_item}")

    def close_connection(self):
        self.connection.close()


if __name__ == "__main__":
    text_item_data = {"datetime": datetime.now(), "title": "text1", "text": "text1"}
    pika_producer = PikaProducer()
    pika_producer.publish_text(TextItem(**text_item_data))
