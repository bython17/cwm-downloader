import requests
from bs4 import BeautifulSoup
from json import loads
from src.scraper.lecture_scraper import Lecture  # typing: ignore
from src.scraper._scraper import Scraper


class Course(Scraper):
    def get_name(self) -> str:
        return ''

    def get_lectures(self) -> list[Lecture]:
        pass
        # return [Lecture(), self.request_session)]
