from typing import Literal

LectureType = Literal['video', 'text']


class Lecture:
    def __init__(self, lecture_url):
        self.lecture_url = lecture_url

    def get_download_urls(self) -> list[str]:
        return ['something']

    def get_lecture_name(self) -> str:
        return 'something'

    def get_lecture_type(self) -> LectureType:
        return 'video'

    def is_valid(self) -> bool:
        return True
