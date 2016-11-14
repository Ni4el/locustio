from locust import HttpLocust, TaskSet, task


class GeneralWebsiteTasks(TaskSet):
    @task(1)
    def index(self):
        self.client.get("/")

    @task(2)
    class CompetitionsTasks(TaskSet):
        min_wait = 100
        max_wait = 300

        @task(3)
        def champions_league(self):
            self.client.get("/news/1716/champions-league")

        @task(5)
        def icc_2016(self):
            self.client.get("/news/24092/icc-2016")

        @task(1)
        def stop(self):
            self.interrupt()


class WebsiteUser(HttpLocust):
    host = 'http://www.goal.com/en'
    task_set = GeneralWebsiteTasks
    min_wait = 2000
    max_wait = 5000
