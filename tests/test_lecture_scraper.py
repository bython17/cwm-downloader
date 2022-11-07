from typing import Any, Dict
from cwm_downloader.scraper.lecture_scraper import Lecture, LectureType
from cwm_downloader.utils import sterialize_file_or_folder
import pytest


testing_urls: Dict[str, Dict[str, Any]] = {
    'https://codewithmosh.com/courses/ultimate-c-plus-plus-part1/lectures/42187090': {
        'downloadables': None,
        'name': '3- Getting Help',
        'number': '3',
        'type': 'text'
    },  # C++ Course text
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
    # 'https://codewithmosh.com/courses/357787/lectures/13898953': {
    #     'downloadables': {'react-advanced.zip': 'https://cdn.fs.teachablecdn.com/q39fCl2ASVi4B632lK4Q'},
    #     'resource_name': '2- resource_react-advanced.zip',
    #     'name': '2- Source Code',
    #     'number': '2',
    #     'type': 'text'
    # },  # React Course doesn't see to work so we're gonne skip on that
    'https://codewithmosh.com/courses/783424/lectures/14779974': {
        'downloadables': {'5- Setting Up the Development Environment.mp4': 'https://cdn.fs.teachablecdn.com/vsdryTMASqYUgPm4nMRQ', 'Source Code.zip': 'https://cdn.fs.teachablecdn.com/wr9x3CGyQb2zk5nCObT5'},
        'resource_name': '5- resource_Source Code.zip',
        'name': '5- Setting Up the Development Environment',
        'number': '5',
        'type': 'video'
    },  # Redux coure 5 (resource within a video)
    'https://codewithmosh.com/courses/ultimate-c-plus-plus-part1/lectures/42187134': {
        'downloadables': {'1- Getting Started with C++.pdf': 'https://cdn.fs.teachablecdn.com/vlVGa4CsQzKmJbDhgoUw'},
        'resource_name': '6- resource_Getting Started with C++.pdf',
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
def test_get_name(lecture_obj: Lecture, expected: str):
    assert str(lecture_obj) == expected


@pytest.mark.parametrize('lecture_obj, expected', [
    (url, details['downloadables']) for url, details in testing_urls.items()
], indirect=['lecture_obj'])
def test_get_download_names_and_urls(lecture_obj: Lecture, expected: Dict[str, str] | None):
    assert lecture_obj.get_download_names_and_urls() == expected


@pytest.mark.parametrize('lecture_obj, expected', [
    (url, details['number']) for url, details in testing_urls.items()
], indirect=['lecture_obj'])
def test_get_lecture_number(lecture_obj: Lecture, expected: str | None):
    assert lecture_obj.get_lecture_number() == expected


@pytest.mark.parametrize('lecture_obj, downloadables, expected', [
    (url, details['downloadables'], details['resource_name']) for url, details in testing_urls.items() if 'resource_name' in details
], indirect=['lecture_obj'])
def test_get_resource_name(lecture_obj: Lecture, downloadables: Dict[str, str], expected: str):
    for resource_name in downloadables.keys():
        if resource_name.split('.')[-1] != 'mp4':
            assert lecture_obj.get_resource_name(resource_name) == expected


@pytest.mark.parametrize('lecture_obj, expected', [
    (url, details['type']) for url, details in testing_urls.items()
], indirect=['lecture_obj'])
def test_get_type(lecture_obj: Lecture, expected: LectureType):
    assert lecture_obj.get_type() == expected


@pytest.mark.parametrize('filename, expected', [
    (r'a|<b>cd?.html', 'abcd.html'),
    (r'a//.\.zip', 'a.zip'),
    ('something ... zip.  .', 'something.zip')
])
def test_sterilize_filenames(filename: str, expected: str):
    assert sterialize_file_or_folder(filename) == expected
