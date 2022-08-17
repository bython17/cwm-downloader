import pytest
from src.scraper import Scraper

course_urls = [
  'https://codewithmosh.com/courses/enrolled/783424/', # Redux Course
  'https://codewithmosh.com/courses/enrolled/1857029', # C++ Course
  'https://codewithmosh.com/courses/enrolled/357787', # React Course
  'https://codewithmosh.com/courses/enrolled/580597', # Java Course
]

@pytest.fixture(scope="module", params=course_urls)
def scraper_obj(request):
  return Scraper(request.param)