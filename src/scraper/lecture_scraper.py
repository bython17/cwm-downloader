from typing import Literal
from src.scraper._scraper import Scraper

LectureType = Literal['video', 'text']


class Lecture(Scraper):
    def get_download_urls(self) -> list[str]:
        return ['something']

    def get_name(self) -> str:
        lecture_name = self.select_element(self.element_selectors.lecture_names, single=True)
        return lecture_name.get_text(strip=True)

    def get_type(self) -> bool:
        pass
