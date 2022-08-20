import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup, Tag
from src.utils import handle_network_errors
from src.scraper.element_selectors import ElementSelectors


class IncorrectUrlError(Exception):
    pass


class ElementNotFoundError(Exception):
    pass


class Scraper(ABC):
    base_url = "https://codewithmosh.com/courses"
    element_selectors = ElementSelectors

    def __init__(self, url: str, request_session: requests.Session, timeout: int = 60):
        self.url = url
        self.timeout = timeout
        self.session = request_session
        self.__soup = None

    @property
    def soup(self):
        if self.__soup is None:
            self.__soup = self.make_soup()
        return self.__soup

    @handle_network_errors
    def make_soup(self):
        content = self.session.get(self.url, timeout=self.timeout)
        return BeautifulSoup(content.content, 'html.parser')

    def select_element(self, element: ElementSelectors, source: Tag | BeautifulSoup | None = None, single: bool = False, raise_if_not_found: bool = True):
        source = source if source is not None else self.soup
        for selector in element.value:
            tag_list_or_tag = list(source.select(selector)) if not single else source.select_one(selector)
            if tag_list_or_tag:
                return tag_list_or_tag
        if raise_if_not_found:
            raise ElementNotFoundError(f'The element with the selector ({selector}) is invalid!, The site might be updated...')

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, new_url: str):
        self.__url = self.validate_url(new_url)
        if not self.__url:
            raise (IncorrectUrlError(f'{new_url} is not mosh\'s url.'))

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

    def __str__(self):
        return self.get_name()