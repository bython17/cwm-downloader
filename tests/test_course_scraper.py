from src.scraper.course_scraper import Course
from src.scraper._scraper import IncorrectUrl
import pytest

course_urls = [
    'https://codewithmosh.com/courses/enrolled/783424',  # Redux Course
    'https://codewithmosh.com/courses/enrolled/1857029',  # C++ Course
    'https://codewithmosh.com/courses/enrolled/357787',  # React Course
    'https://codewithmosh.com/courses/enrolled/580597',  # Java Course
]


@pytest.fixture(scope="function", params=course_urls)
def course_obj(request, request_session):
    return Course(request.param, request_session)


def test_is_validate_url_fails(request_session):
    with pytest.raises(IncorrectUrl):
        Course('https://afakewebsite/enrolled/invalid', request_session)


@pytest.mark.parametrize('course_url, expected', [
    ('https://codewithmosh.com/courses/enrolled/580597', 'https://codewithmosh.com/courses/580597'),
    ('https://code withmosh.com/ courses/e nrolled/580597', 'https://codewithmosh.com/courses/580597'),
    ('https://codewithmosh.com/courses/580597/', 'https://codewithmosh.com/courses/580597')
])
def test_is_validate_url_passes(course_url: str, expected: str, request_session):
    url = Course(course_url, request_session).url
    assert url == expected
