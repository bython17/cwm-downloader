from pathlib import Path
from typing import List
from src.scraper.lecture_scraper import Lecture
from src.scraper._scraper import Scraper
from rich.progress import Progress
from urllib.parse import urljoin


class Course(Scraper):
    @staticmethod
    def slice_list(list_obj: List, index: List[int]) -> List:
        start, end = index
        if end == -1:
            return list_obj[start:]
        return list_obj[start:end+1]

    # cwm-downloader url --sections 3-5 --lectures 3-34

    def download(self, base_dir: Path, progress_bar: Progress, sections: List[int] = [0, -1], lectures: List[int] = [0, -1], chunk_size: int = 4096) -> None:
        sections_and_lectures = self.get_lectures()
        filtered_sections: List[str] = self.slice_list(list(sections_and_lectures.keys()), sections)
        for section in filtered_sections:
            filtered_lectures: List[Lecture] = self.slice_list(sections_and_lectures[section], lectures)
            section_path = base_dir / section
            section_path.mkdir(exist_ok=True)
            for lecture in filtered_lectures:
                lecture.download(section_path, progress_bar, chunk_size)

    def get_lectures(self):
        section_containers = self.select_element(self.element_selectors.section_containers)
        section_lectures = {
            self.select_element(self.element_selectors.section_names, section_container, single=True).get_text(strip=True): [
                Lecture(urljoin(self.base_url, lecture.get('href')), self.session, self.timeout) for lecture in self.select_element(self.element_selectors.lecture_anchor_tags, section_container)
            ] for section_container in section_containers
        }
        return section_lectures

    def get_name(self):
        course_name = self.select_element(self.element_selectors.course_name, single=True)
        return course_name.get_text(strip=True)

    def __iter__(self):
        return self.get_lectures().items()
