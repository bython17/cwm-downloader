"""
This modules provides an Abstract Base class for the Lecture and 
Course classes.
"""

import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup, Tag
from cwm_downloader.exceptions import IncorrectUrlError, ElementNotFoundError
from cwm_downloader.utils import handle_network_errors
from cwm_downloader.scraper.element_selectors import ElementSelectors
from functools import cached_property


class Scraper(ABC):
    """
    This is the abstract base class that contains alot of boiler plate code
    for Lecture and Course.
    """

    base_url = "https://members.codewithmosh.com"
    # ElementSelectors is an enum containing all the css selectors needed
    # To scrape the site.
    element_selectors = ElementSelectors

    def __init__(self, url: str, request_session: requests.Session, timeout: int = 60):
        """
        Constructor

        :param url: The url of the site
        :param request_session: A requests.Session object
        :timeout: The amount of time to wait for a package before terminating the request 
        """
        # Assigning some attributes to the parameters
        self.url = url
        self.timeout = timeout
        self.session = request_session

    # This is property that uses lazy loading to load the soup. This is
    # because making a soup is expensive so once you lazy load it you can
    # reuse it again and again without re requesting.
    @cached_property
    def soup(self):
        return self.make_soup()

    @handle_network_errors
    def make_soup(self):
        """ Makes a BeautifulSoup object using the url and timeout attributes."""
        content = self.session.get(self.url, timeout=self.timeout)
        return BeautifulSoup(content.content, 'html.parser')

    def select_element(self, element: ElementSelectors, source: Tag | BeautifulSoup | None = None, single: bool = False, raise_if_not_found: bool = True):
        """
        Select an element given the element_selector

        :param element: An enum property i.e The list with many css selectors
        :param source: The source Tag or BeautifulSoup object that is used to search the element  parameter in.
        :param single: If True, return a single element rather than a list of element(s)
        :param raise_if_not_found: If False, don't raise an ElementNotFoundError even if that element couldn't be found on the site. 
        """

        # Set the source to self.soup if the source is not given
        source = source if source is not None else self.soup
        # Now we are looping over the selectors that are given to us
        # We are using a list of selectors because we can go move to another one
        # If some fails
        for selector in element.value:
            # Select a Tag(using source.select_one) or a ResultSet(using source.select) accoring to the
            # single parameter.
            tag_list_or_tag = list(source.select(selector)) if not single else source.select_one(selector)
            # only return the element(s) if it is not none i.e
            # If it is found
            if tag_list_or_tag:
                return tag_list_or_tag
        if raise_if_not_found:
            raise ElementNotFoundError(f'The element with the selector ({selector}) is invalid!, The site might be updated...')

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, new_url: str):
        # Validate each url before setting it
        self.__url = self.validate_url(new_url)
        if not self.__url:
            # This means the validation failed so raise an error
            raise IncorrectUrlError(f'{new_url} is not mosh\'s url.')

    def validate_url(self, url: str) -> str | bool:
        """
        Validates and parses a url to a managable form for the downloaders

        :param url: The url to be validated
        """

        # Replace any whitespace in the url
        url = url.replace(' ', '')

        # Check if the base url is inside the url and if it is not
        # return False which means that the validation failed.
        if self.base_url not in url:
            return False

        # Replace the "/enrolled" text from the url. because that exists
        # only on the courses
        url = url.replace('/enrolled', '')
        # Also remove the final / for safety purposes
        if url.endswith('/'):
            url = url[:len(url)-1]
        return url

    @abstractmethod
    def get_name(self) -> str:
        # Must be implemented by child classes to get the __str__ functionality
        pass

    def __str__(self):
        return self.get_name()
