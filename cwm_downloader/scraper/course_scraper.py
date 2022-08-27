from pathlib import Path
from typing import List, Union
from cwm_downloader.scraper.lecture_scraper import Lecture
from cwm_downloader.scraper._scraper import Scraper
from urllib.parse import urljoin
from cwm_downloader.utils import render_message


class Course(Scraper):
    @staticmethod
    def slice_list(list_obj: List, index: List[Union[int, str]]) -> List:
        for i, value in enumerate(index):
            if value == 'start':
                index[i] = 0
            if value == 'end':
                index[i] = len(list_obj)
        start, end = index
        return list_obj[start-1:end+1]  # type: ignore

    def download(self, base_dir: Path, sections: List[Union[int, str]] = ['start', 'end'], lectures: List[Union[int, str]] = ['start', 'end'], chunk_size: int = 4096, noconfirm=False) -> None:
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
                lecture.download(section_dir, chunk_size, noconfirm)

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
