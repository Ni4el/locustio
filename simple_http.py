from locust import HttpLocust, TaskSet, task


class WebsiteTasks(TaskSet):
    @task(1)
    def index(self):
        self.client.get("/")

    @task(2)
    def champions_league(self):
        self.client.get("/news/1716/champions-league")


class WebsiteUser(HttpLocust):
    host = 'http://www.goal.com/en'
    task_set = WebsiteTasks
    min_wait = 2000
    max_wait = 5000
