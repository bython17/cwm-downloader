from src.scraper.lecture_scraper import Lecture
import pytest

lecture_urls = [
    'https://codewithmosh.com/courses/783424/lectures/14779988',  # Redux Course 1
    'https://codewithmosh.com/courses/ultimate-c-plus-plus-part1/lectures/42187035',  # C++ Course 1
    'https://codewithmosh.com/courses/ultimate-c-plus-plus-part1/lectures/42187090',  # C++ Course text
    'https://codewithmosh.com/courses/357787/lectures/5634517',  # React Course text
]


@pytest.mark.parametrize('lecture_url, expected', [
    ('https://codewithmosh.com/courses/783424/lectures/invalid', False),
    ('https://codewithmosh.com/courses/783424/lectures/14779988', True)
])
def test_lecture_is_valid(lecture_url: str, expected: bool):
    assert Lecture(lecture_url).is_valid() == expected


@pytest.fixture(scope="module", params=lecture_urls)
def lecture_obj(request):
    return Lecture(request.param)
