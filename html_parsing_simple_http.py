import random
from locust import HttpLocust, TaskSet, task
from pyquery import PyQuery


class BrowseDocumentation(TaskSet):
    def on_start(self):
        # assume all users arrive at the index page
        self.index_page()
        self.urls_on_current_page = self.toc_urls

    @task(10)
    def index_page(self):
        r = self.client.get("/")
        pq = PyQuery(r.content)
        link_elements = pq(".toctree-wrapper a.internal")
        self.toc_urls = [l.attrib["href"] for l in link_elements]

    @task(50)
    def load_page(self, url=None):
        url = random.choice(self.toc_urls)
        r = self.client.get(url)
        pq = PyQuery(r.content)
        link_elements = pq("a.internal")
        self.urls_on_current_page = [l.attrib["href"] for l in link_elements]

    @task(30)
    def load_sub_page(self):
        url = random.choice(self.urls_on_current_page)
        r = self.client.get(url)


class AwesomeUser(HttpLocust):
    task_set = BrowseDocumentation
    host = "http://docs.locust.io/en/latest/"

    # we assume someone who is browsing the Locust docs,
    # generally has a quite short waiting time (between
    # 2 and 5 seconds)
    min_wait = 2 * 1000
    max_wait = 5 * 1000