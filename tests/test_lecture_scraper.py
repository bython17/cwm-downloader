from typing import Any, Dict
from src.scraper.lecture_scraper import Lecture
import pytest

testing_urls: Dict[str, Dict[str, Any]] = {
    'https://codewithmosh.com/courses/783424/lectures/14779988': {
        'downloadables': None,
        'name': '1- Welcome',
        'number': '1',
        'type': 'video'
    },  # Redux Course 1 (No download buton)
    'https://codewithmosh.com/courses/ultimate-c-plus-plus-part1/lectures/42187035': {
        'downloadables': {'1-_Welcome.mp4': 'https://cdn.fs.teachablecdn.com/KwO41woZSmSiN2ZzKqjA'},
        'name': '1- Welcome',
        'number': '1',
        'type': 'video'
    },  # Cpp course #1
    'https://codewithmosh.com/courses/ultimate-c-plus-plus-part1/lectures/42187090': {
        'downloadables': None,
        'name': '3- Getting Help',
        'number': '3',
        'type': 'text'
    },  # C++ Course text
    'https://codewithmosh.com/courses/357787/lectures/13898953': {
        'downloadables': {'react-advanced.zip': 'https://cdn.fs.teachablecdn.com/q39fCl2ASVi4B632lK4Q'},
        'resource_name': '2- resource_react-advanced.zip',
        'name': '2- Source Code',
        'number': '2',
        'type': 'text'
    },  # React Course text
    'https://codewithmosh.com/courses/783424/lectures/14779974': {
        'downloadables': {'5- Setting Up the Development Environment.mp4': 'https://cdn.fs.teachablecdn.com/vsdryTMASqYUgPm4nMRQ', 'Source Code.zip': 'https://cdn.fs.teachablecdn.com/wr9x3CGyQb2zk5nCObT5'},
        'resource_name': '5- Source Code.zip',
        'name': '5- Setting Up the Development Environment',
        'number': '5',
        'type': 'video'
    },  # Redux coure 5 (resource within a video)
    'https://codewithmosh.com/courses/ultimate-c-plus-plus-part1/lectures/42187134': {
        'downloadables': {'1- Getting Started with C++.pdf': 'https://cdn.fs.teachablecdn.com/vlVGa4CsQzKmJbDhgoUw'},
        'resource_name': '6- Getting Started with C++.pdf',
        'name': '6- Summary',
        'number': '6',
        'type': 'text'
    }
}


@pytest.fixture(scope="function")
def lecture_obj(request, request_session):
    return Lecture(request.param, request_session)


@pytest.mark.parametrize('lecture_obj, expected', [
    (url, details['name']) for url, details in testing_urls.items()
], indirect=['lecture_obj'])
def test_get_name(lecture_obj, expected):
    assert str(lecture_obj) == expected


@pytest.mark.parametrize('lecture_obj, expected', [
    (url, details['downloadables']) for url, details in testing_urls.items()
], indirect=['lecture_obj'])
def test_get_download_names_and_urls(lecture_obj, expected):
    assert lecture_obj.get_download_names_and_urls() == expected
