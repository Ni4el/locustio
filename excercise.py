import random

from locust import HttpLocust, TaskSet, task, main
from pyquery import PyQuery


class Excercise(TaskSet):

    def on_start(self):
        # assume all users arrive at the index page
        r = self.client.get("/")
        pq = PyQuery(r.content)
        orginal_title1 = pq(".pageHeaderLogo .serviceName a")
        self.orginal_title = [l.attrib['href'] for l in orginal_title1]
        current_news = pq(".boxDriverInList a")
        self.current_news_urls = [l.attrib['href'] for l in current_news]
        main_news = pq(".stream .listItem a")
        self.main_news_urls = [l.attrib['href'] for l in main_news]
        navibar_elements = pq(".mainMenu a")
        self.navibar_urls = [l.attrib['href'] for l in navibar_elements]
        self.title = "Wiadomo&#347;ci"

    @task(5)
    def HomePage(self):
        with self.client.get("/", catch_response=True) as response:
            if self.parent.orginal_title == self.title:
                response.failure('Something goes wrong')


    @task(3)
    def NavibarLinks(self):
        url = random.choice(self.navibar_urls)
        self.client.get(url)

    @task(1)
    class RandomNews(TaskSet):
        min_wait = 500
        max_wait = 800

        @task(30)
        def random_current_news(self):
            url = random.choice(self.parent.current_news_urls)
            self.client.get(url)

        @task(20)
        def random_main_news(self):
            url = random.choice(self.parent.main_news_urls)
            self.client.get(url)

        @task(10)
        def stop(self):
            self.interrupt()

class WebsiteUser(HttpLocust):
    host = 'http://wiadomosci.onet.pl/'
    task_set = Excercise
    min_wait = 1000
    max_wait = 2000

main.main()