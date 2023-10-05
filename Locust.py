from locust import HttpUser, task, between


class MyUser(HttpUser):
    wait_time = between(1, 3)  # Время ожидания между запросами (в секундах)

    @task
    def post_message(self):
        headers = {'Content-Type': 'application/json'}
        data = {'msg_id': 1111}
        response = self.client.post('/post-message', json=data, headers=headers)

        if response.status_code == 200:
            print('Message posted successfully')

    # Добавьте другие задачи, если необходимо
