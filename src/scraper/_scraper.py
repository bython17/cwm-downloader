from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from src.utils import get_element_selectors


class UrlNotFoundError(Exception):
    pass


class Scraper(ABC):
    def __init__(self, url: str, timeout: int = 60):
        self.url = url

    @property
    def ELEMENT_SELECTORS(self):
        self.element_selectors = get_element_selectors()
        return self.element_selectors

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, new_url):
        if not self.is_valid_url():
            raise UrlNotFoundError(f'{new_url} is not found')
        self.__url = new_url

    @abstractmethod
    def is_valid_url(self) -> bool:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass
