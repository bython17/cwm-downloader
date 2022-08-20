from src.scraper.course_scraper import Course
from src.scraper._scraper import IncorrectUrlError
import pytest

course_urls = [
    'https://codewithmosh.com/courses/783424/lectures/14779988',  # Redux Course
    'https://codewithmosh.com/courses/ultimate-c-plus-plus-part1/lectures/42187035',  # C++ Course
    'https://codewithmosh.com/courses/357787/lectures/5634517',  # React Course
    'https://codewithmosh.com/courses/580597/lectures/10548877',  # Java Course
]


@pytest.fixture(scope="function", params=course_urls)
def course_obj(request, request_session):
    return Course(request.param, request_session)


def test_is_validate_url_fails(request_session):
    with pytest.raises(IncorrectUrlError):
        Course('https://afakewebsite/enrolled/invalid', request_session)


@pytest.mark.parametrize('course_url, expected', [
    ('https://codewithmosh.com/courses/enrolled/580597', 'https://codewithmosh.com/courses/580597'),
    ('https://code withmosh.com/ courses/e nrolled/580597', 'https://codewithmosh.com/courses/580597'),
    ('https://codewithmosh.com/courses/580597/', 'https://codewithmosh.com/courses/580597')
])
def test_is_validate_url_passes(course_url: str, expected: str, request_session):
    url = Course(course_url, request_session).url
    assert url == expected


def test_get_course_name(course_obj: Course):
    assert str(course_obj) != ''
    assert not str(course_obj).isspace()
