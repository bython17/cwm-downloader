from typing import Generator
from src.scraper.lecture_scraper import Lecture
from src.scraper._scraper import Scraper
from rich.progress import Progress


class Course(Scraper):
    def download(self, progress_bar: Progress) -> None:
        pass

    def get_lectures(self):
        section_containers = self.select_element(self.element_selectors.section_containers)
        section_lectures = {
            self.select_element(self.element_selectors.section_names, section_container, single=True).get_text(strip=True): self.select_element(self.element_selectors.lecture_anchor_tags, section_container).get('href') for section_container in section_containers
        }
        return section_lectures

    def get_name(self):
        course_name = self.select_element(self.element_selectors.course_name, single=True)
        return course_name.get_text(strip=True)

    def __iter__(self):
        return self.get_lectures().items()
