from src.scraper.lecture_scraper import Lecture
from src.scraper._scraper import Scraper


class Course(Scraper):
    def get_lectures(self) -> list[Lecture]:
        pass

    def get_name(self):
        course_name = self.select_element(self.element_selectors.course_name, single=True)
        return course_name.get_text(strip=True)
