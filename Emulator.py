from flask import Flask, request, jsonify
import time

app = Flask(__name__)


@app.route('/post-message', methods=['POST'])
def post_message():
    data = request.get_json()
    msg_id = data.get('msg_id')
    timestamp = int(time.time())
    response = {
        'msg_ID': f'{msg_id}',
        'timestamp': timestamp
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run()