from src.scraper.lecture_scraper import Lecture
from src.scraper._scraper import Scraper


class Course(Scraper):
    def get_lectures(self) -> list[Lecture]:
        lecture_list = self.select_element(self.element_selectors.lecture_anchor_tags)
        return [Lecture(lecture.get('href'), self.session) for lecture in lecture_list]

    def get_name(self):
        course_name = self.select_element(self.element_selectors.course_name, single=True)
        return course_name.get_text(strip=True)

    def __iter__(self):
        return iter(self.get_lectures())

    def __len__(self):
        return len(self.get_lectures())
