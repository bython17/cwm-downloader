import requests
from bs4 import BeautifulSoup
from json import loads
from src.scraper.lecture_scraper import Lecture
from src.utils import get_element_selectors

ELEMENT_SELECTORS = get_element_selectors()


class Course:
    def __init__(self, course_url):
        self.course_url = course_url

    def get_course_name(self) -> str:
        return ''

    def get_lectures(self) -> list[Lecture]:
        return [Lecture('')]

    def is_valid(self) -> bool:
        return False
