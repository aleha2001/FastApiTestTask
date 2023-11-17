import pika
import asyncio
import json


def process_text(ch, method, properties, body):
    data = json.loads(body)
    print(f"message recieved {data}")
    x_count = data["text"].count("X")
    print(f"data processed {x_count}")
    # TODO: insert into db


def consume():
    print("start consuming")
    connections_params = pika.ConnectionParameters("localhost")
    connection = pika.BlockingConnection(connections_params)
    chanel = connection.channel()
    chanel.queue_declare(queue="texts")
    chanel.basic_consume(queue="texts", auto_ack=True, on_message_callback=process_text)
    chanel.start_consuming()


if __name__ == "__main__":
    consume()
