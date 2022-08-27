from pathlib import Path
from typing import List, Union
from src.scraper.lecture_scraper import Lecture
from src.scraper._scraper import Scraper
from urllib.parse import urljoin
from src.utils import render_message


class Course(Scraper):
    @staticmethod
    def slice_list(list_obj: List, index: List[Union[int, str]]) -> List:
        start, end = index
        if end == 'end':
            end = len(list_obj)
        if start == 'start':
            start = 0

        return list_obj[start:end+1]  # type: ignore

    def download(self, base_dir: Path, sections: List[Union[int, str]] = ['start', 'end'], lectures: List[Union[int, str]] = ['start', 'end'], chunk_size: int = 4096) -> None:
        sections_and_lectures = self.get_lectures()
        filtered_sections: List[str] = self.slice_list(list(sections_and_lectures.keys()), sections)
        course_dir = base_dir / str(self)
        course_dir.mkdir(exist_ok=True)
        for section in filtered_sections:
            filtered_lectures: List[Lecture] = self.slice_list(sections_and_lectures[section], lectures)
            section_dir = course_dir / section
            section_dir.mkdir(exist_ok=True)
            render_message('info', f'Starting section [bold blue]{section}', start='\n', end='\n\n')
            for lecture in filtered_lectures:
                lecture.download(section_dir, chunk_size)

    def get_lectures(self):
        section_containers = self.select_element(self.element_selectors.section_containers)
        section_lectures = {
            f"{index + 1}- {self.select_element(self.element_selectors.section_names, section_container, single=True).get_text(strip=True)}": [
                Lecture(urljoin(self.base_url, lecture.get('href')), self.session, self.timeout) for lecture in self.select_element(self.element_selectors.lecture_anchor_tags, section_container)
            ] for index, section_container in enumerate(section_containers)
        }
        return section_lectures

    def get_name(self):
        course_name = self.select_element(self.element_selectors.course_name, single=True)
        return course_name.get_text(strip=True)

    def __iter__(self):
        return self.get_lectures().items()
