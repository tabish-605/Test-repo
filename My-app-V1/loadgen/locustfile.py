from locust import HttpUser, task, between
from random import choice, random

class Shopper(HttpUser):
    wait_time = between(1, 3)

    @task(2)
    def list_products(self):
        self.client.get('/api/products')

    @task(3)
    def add_cart(self):
        pid = choice([1,2,3])
        self.client.post('/api/cart/add', json={"product_id": pid, "quantity": 1})

    @task(1)
    def checkout(self):
        fail = random() < 0.1
        url = '/api/checkout?simulate_failure=true' if fail else '/api/checkout'
        self.client.post(url, json={})
