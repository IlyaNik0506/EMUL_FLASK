from locust import HttpUser, task, between
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import random
import time

token = "SJbo0hnuMCmAonUITNcJNRX7fAiJFlF7hIm_BZw0SF-XCqKaKxBof2rC0ImBkI5j1xrM6zm0L3MH87kQPXtvBA=="
org = "QE"
bucket = "QE_VTB"
url = "http://localhost:8086"  # Замените на URL вашего InfluxDB 2

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)


class MyUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def post_message(self):
        x = random.randrange(10000, 200000)
        headers = {'Content-Type': 'application/json'}
        data = {'msg_id': x}
        response = self.client.post('/post-message', json=data, headers=headers)
        print(response.text)
        if response.status_code == 200:
            print('Сообщение успешно отправлено')

        point = Point("locust_metrics").tag("user", self.__class__.__name__).field("response_time", response.elapsed.total_seconds())
        write_api.write(bucket=bucket, org=org, record=point)

    def on_start(self):
        stages = [
            {'duration': 3, 'rps': 0.5},
            {'duration': 3, 'rps': 1.0},
            {'duration': 3, 'rps': 1.5},
            {'duration': 3, 'rps': 2.0},
            {'duration': 3, 'rps': 2.5},
        ]

        for stage in stages:
            self.environment.runner.start(1, spawn_rate=stage['rps'])
            time.sleep(stage['duration'])
            self.environment.runner.stop()



