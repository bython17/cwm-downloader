from typing import Literal
from src.scraper._scraper import Scraper

LectureType = Literal['video', 'text']


class Lecture(Scraper):
    def get_download_urls(self) -> list[str]:
        return ['something']

    def get_name(self) -> str:
        return 'something'

    def get_lecture_type(self) -> LectureType:
        return 'video'
