import requests
from bs4 import BeautifulSoup
from json import loads
from src.scraper.lecture_scraper import Lecture  # typing: ignore
from src.scraper._scraper import Scraper


class Course(Scraper):
    def __init__(self, course_url):
        self.course_url = course_url

    def get_name(self) -> str:
        return ''

    def get_lectures(self) -> list[Lecture]:
        return [Lecture('')]

    def is_valid_url(self) -> bool:
        return True
