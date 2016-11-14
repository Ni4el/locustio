from locust import HttpLocust, TaskSet, task


class WebsiteTasks(TaskSet):
    @task(1)
    def index(self):
        self.client.get("/")

    @task(1)
    def about(self):
        self.client.get("/store")


class WebsiteUser(HttpLocust):
    host = 'http://oddsstore.rball.com'
    task_set = WebsiteTasks
    min_wait = 2000
    max_wait = 5000
