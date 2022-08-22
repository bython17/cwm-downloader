from typing import List
from src.scraper.lecture_scraper import Lecture
from src.scraper._scraper import Scraper
from rich.progress import Progress
from urllib.parse import urljoin


class Course(Scraper):
    @staticmethod
    def parse_index(index: List[int], index_name: str) -> str:
        start, end = index
        final_string = index_name + ' {}'
        if start == 0 and end == -1:
            return final_string.format('').strip()
        if start != 0 and end == -1:
            return final_string.format(f'(From {start})')
        if start == 0 and end != -1:
            return final_string.format(f'(1 to {end})')
        return final_string.format(f'({start} - {end})')

    def download(self, progress_bar: Progress, sections: List[int] = [0, -1], lectures: List[int] = [0, -1]) -> None:

        course_task_id = progress_bar.add_task('course download', start=False, filename=str(self))

    def get_lectures(self):
        section_containers = self.select_element(self.element_selectors.section_containers)
        section_lectures = {
            self.select_element(self.element_selectors.section_names, section_container, single=True).get_text(strip=True): [
                urljoin(self.base_url, lecture.get('href')) for lecture in self.select_element(self.element_selectors.lecture_anchor_tags, section_container)
            ] for section_container in section_containers
        }
        return section_lectures

    def get_name(self):
        course_name = self.select_element(self.element_selectors.course_name, single=True)
        return course_name.get_text(strip=True)

    def __iter__(self):
        return self.get_lectures().items()
