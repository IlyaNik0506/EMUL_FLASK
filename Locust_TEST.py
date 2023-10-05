from locust import HttpUser, task, between, LoadTestShape
import random
import time


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


class TESsT(LoadTestShape):
    stages = [
        {'duration': 10, 'users': 10, 'spawn_rate': 5},
        {'duration': 10, 'users': 20, 'spawn_rate': 5},
        {'duration': 10, 'users': 30, 'spawn_rate': 1},
        {'duration': 10, 'users': 40, 'spawn_rate': 1},
        {'duration': 10, 'users': 50, 'spawn_rate': 1},
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data
        return None



