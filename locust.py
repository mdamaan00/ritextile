import time
from locust import HttpUser,task,between

class WebsiteUser(HttpUser):
    wait_time = between(1,5)

    @task
    def home_page(self):
        self.client.get(url="")
    
    @task
    def products_page(self):
        self.client.get(url="products/")

    @task
    def contact_page(self):
        self.client.get(url="contactus/")

    @task
    def prodview_page(self):
        self.client.get(url="products/2/")

    @task
    def review_page(self):
        self.client.get(url="reviews/2/")