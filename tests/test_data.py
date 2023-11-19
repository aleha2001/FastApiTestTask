import os
import requests
import time
from datetime import datetime


# Function to read sentences from a file
def read_sentences(file_path):
    with open(file_path, "r") as file:
        sentences = file.read().splitlines()
    return sentences


# Function to send requests to the FastAPI endpoint
def send_requests(sentences):
    base_url = "http://0.0.0.0:8000"
    for i, sentence in enumerate(sentences):
        payload = {
            "datetime": datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f"),
            "title": f"Title of sentence_{i}",
            "text": sentence,
        }
        print(payload)
        response = requests.post(f"{base_url}/text", json=payload)
        print(f"Response: {response.status_code}, {response.json()}")

        time.sleep(3)


if __name__ == "__main__":
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(cur_dir, "data/text.txt")
    sentences = read_sentences(file_path)

    if sentences:
        send_requests(sentences)
    else:
        print("No sentences found in the file.")
