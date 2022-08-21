from src.scraper.course_scraper import Course
from src.scraper._scraper import IncorrectUrlError
import pytest

testing_urls = {
    'https://codewithmosh.com/courses/783424/lectures/14779988': {
        'name': 'The Ultimate Redux Course'
    },  # Redux Course
    'https://codewithmosh.com/courses/ultimate-c-plus-plus-part1/lectures/42187035': {
        'name': 'Ultimate C++ Part 1: Fundamentals'
    },  # C++ Course
    'https://codewithmosh.com/courses/357787/lectures/5634517': {
        'name': 'Mastering React'
    },  # React Course
    'https://codewithmosh.com/courses/580597/lectures/10548877': {
        'name': 'Ultimate Java Part 1: Fundamentals'
    },  # Java Course
}


@pytest.fixture(scope="function")
def course_obj(request, request_session):
    return Course(request.param, request_session)


# Test validate_url function defined in _scraper.py
def test_is_validate_url_fails(request_session):
    with pytest.raises(IncorrectUrlError):
        Course('https://afakewebsite/enrolled/invalid', request_session)


@pytest.mark.parametrize('course_obj, expected', [
    ('https://codewithmosh.com/courses/enrolled/580597', 'https://codewithmosh.com/courses/580597'),
    ('https://code withmosh.com/ courses/e nrolled/580597', 'https://codewithmosh.com/courses/580597'),
    ('https://codewithmosh.com/courses/580597/', 'https://codewithmosh.com/courses/580597')
], indirect=['course_obj'])
def test_is_validate_url_passes(course_obj: Course, expected: str):
    assert course_obj.url == expected


@pytest.mark.parametrize('course_obj, expected', [
    (url, details['name']) for url, details in testing_urls.items()
], indirect=['course_obj'])
def test_get_name(course_obj: Course, expected: str):
    assert str(course_obj) == expected


@pytest.mark.parametrize('course_obj', [
    url for url in testing_urls.keys()
], indirect=True)
def test_get_lectures(course_obj: Course):
    lectures = course_obj.get_lectures()
    print(lectures)
    assert len(lectures)
    assert all(len(section) for section in lectures.values())
