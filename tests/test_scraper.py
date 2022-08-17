from src.scraper import Lecture, Course
import pytest

course_urls = [
    'https://codewithmosh.com/courses/enrolled/783424/',  # Redux Course
    'https://codewithmosh.com/courses/enrolled/1857029',  # C++ Course
    'https://codewithmosh.com/courses/enrolled/357787',  # React Course
    'https://codewithmosh.com/courses/enrolled/580597',  # Java Course
]

lecture_urls = [
    'https://codewithmosh.com/courses/783424/lectures/14779988',  # Redux Course 1
    'https://codewithmosh.com/courses/ultimate-c-plus-plus-part1/lectures/42187035',  # C++ Course 1
    'https://codewithmosh.com/courses/ultimate-c-plus-plus-part1/lectures/42187090',  # C++ Course text
    'https://codewithmosh.com/courses/357787/lectures/5634517',  # React Course text
]


@pytest.fixture(scope="module", params=course_urls)
def course_obj(request):
    return Course(request.param)


@pytest.fixture(scope="module", params=lecture_urls)
def lecture_obj(request):
    return Lecture(request.param)


@pytest.mark.parametrize('course_url, expected', [
    ('https://codewithmosh.com/courses/enrolled/invalid', False),
    ('https://codewithmosh.com/courses/enrolled/580597', True)
])
def test_course_is_valid(course_url: str, expected: bool):
    assert Course(course_url).is_valid() == expected


@pytest.mark.parametrize('lecture_url, expected', [
    ('https://codewithmosh.com/courses/783424/lectures/invalid', False),
    ('https://codewithmosh.com/courses/783424/lectures/14779988', True)
])
def test_lecture_is_valid(lecture_url: str, expected: bool):
    assert Lecture(lecture_url).is_valid() == expected


def test_get_course_name(course_obj: Course):
    course_name = course_obj.get_course_name()
    assert course_name and not course_name.isspace()


def test_get_lectures(course_obj: Course):
    lectures = course_obj.get_lectures()
    assert len(lectures)
