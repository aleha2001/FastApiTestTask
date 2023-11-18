import pika
import asyncio
import json
from db.database import SessionLocal
from db.queries import insert_text, get_text
from config.config import Config


class PikaConsumer:
    """
    PikaConsumer class
    """

    def __init__(self):
        connections_creds = pika.PlainCredentials(
            username=Config.rb_user, password=Config.rb_password
        )
        connections_params = pika.ConnectionParameters(
            Config.rb_host, credentials=connections_creds, port=Config.rb_port
        )
        self.connection = pika.BlockingConnection(connections_params)
        self.chanel = self.connection.channel()
        self.chanel.queue_declare(queue="texts")

    @staticmethod
    def process_text(ch, method, properties, body):
        """
        Counts x-s in text and saves to db
        """
        data = json.loads(body)
        print(f"message received {data}")
        x_count = data["text"].count("X")
        print(f"data processed {x_count}")
        insert_text(SessionLocal, data.update({"x_count": x_count}))

    async def consume(self, loop):
        print("start consuming")
        self.chanel.basic_consume(
            queue="texts", auto_ack=True, on_message_callback=self.process_text
        )
        self.chanel.start_consuming()


if __name__ == "__main__":
    pika_consumer = PikaConsumer()
    pika_consumer.consume()
