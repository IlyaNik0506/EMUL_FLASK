from kafka import KafkaProducer
from flask import Flask, request
import time
app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='localhost:9092')

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

    producer.send('postedmessages', value=message)
    return '200 ОК'

if __name__ == '__main__':
    app.run()

