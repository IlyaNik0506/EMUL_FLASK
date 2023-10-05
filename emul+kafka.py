from confluent_kafka import Producer
from flask import Flask, request
import time

app = Flask(__name__)
producer = Producer({'bootstrap.servers': 'localhost:9092'})

@app.route('/post-message', methods=['POST'])
def post_message():
    data = request.get_json()
    msg_id = data['msg_id']
    timestamp = str(int(time.time() * 1000))
    method = request.method
    uri = request.path

    message = {
        "msg_id": msg_id,
        "timestamp": timestamp,
        "method": method,
        "uri": uri
    }

    producer.produce('postedmessages', value=message)
    producer.flush()  # Для уверенности, что все сообщения были отправлены
    return '200 ОК'

if __name__ == '__main__':
    app.run()


