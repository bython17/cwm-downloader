import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from src.utils import get_element_selectors, handle_network_errors


class IncorrectUrl(Exception):
    pass


class Scraper(ABC):
    base_url = "https://codewithmosh.com/courses"

    def __init__(self, url: str, request_session: requests.Session, timeout: int = 60):
        self.url = url
        self.timeout = timeout
        self.soup = self.make_soup(request_session)
        self.request_session = request_session

    @handle_network_errors
    def make_soup(self, session):
        content = session.get(self.url)
        return BeautifulSoup(content.content, 'html.parser')

    @property
    def ELEMENT_SELECTORS(self):
        self.element_selectors = get_element_selectors()
        return self.element_selectors

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, new_url):
        self.__url = self.validate_url(new_url)
        if not self.__url:
            raise (IncorrectUrl(f'{new_url} is not mosh\'s url.'))

    def validate_url(self, url: str) -> str | bool:
        url = url.replace(' ', '')
        # check if it is mosh's website
        if self.base_url not in url:
            return False
        # fix the url
        url = url.replace('/enrolled', '')
        if url.endswith('/'):
            url = url[:len(url)-1]
        return url

    @abstractmethod
    def get_name(self) -> str:
        pass
