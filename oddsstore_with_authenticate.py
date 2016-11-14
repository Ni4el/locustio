from locust import HttpLocust, TaskSet, task

list_of_users = ['pawel@test.com', 'automated@test.com', 'tester@test.com']


def user_generator(list_of_users):
    for user in list_of_users:
        yield user

users_generator = user_generator(list_of_users)


class WebsiteTasks(TaskSet):
    def on_start(self):
        user = users_generator.next()
        print('Will be used {}'.format(user))
        self.client.post("/login/authenticate", {
            "username": user,
            "pwd": "test"
        })

    @task(1)
    def index(self):
        self.client.get("/")

    @task(2)
    def about(self):
        self.client.get("/store")


class WebsiteUser(HttpLocust):
    host = 'http://oddsstore.rball.com'
    task_set = WebsiteTasks
    min_wait = 2000
    max_wait = 5000
