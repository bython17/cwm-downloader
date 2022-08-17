import requests
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, course_url):
        self.course_url = course_url

    def get_course_name(self):
        return ''

    def get_lecture_name_url(self):
        return [()]
