import json
import pika
import asyncio
from models import TextItem
from datetime import datetime


def publish_text(text_item: TextItem):
    text_item_json = json.dumps(text_item.model_dump(), indent=4, sort_keys=True, default=str)
    connections_params = pika.ConnectionParameters("localhost")
    connection = pika.BlockingConnection(connections_params)
    chanel = connection.channel()
    chanel.queue_declare(queue="texts")
    chanel.basic_publish(exchange="", routing_key="texts", body=text_item_json)
    print(f"sent text: {text_item}")
    connection.close()


if __name__ == "__main__":
    text_item_data = {"datetime": datetime.now(), "title": "text1", "text": "text1"}
    publish_text(TextItem(**text_item_data))
