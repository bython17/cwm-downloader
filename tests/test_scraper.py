def test_get_course_name(scraper_obj):
    course_name: str = scraper_obj.get_course_name()
    assert course_name is not None
    assert course_name and not course_name.isspace()


def test_get_lecture_name_url(scraper_obj):
    lecture_name_urls: list = scraper_obj.get_lecture_name_url()
    assert lecture_name_urls is not None and len(lecture_name_urls)
    assert type(lecture_name_urls[0]) == tuple and len(lecture_name_urls[0]) == 2
    assert lecture_name_urls[0][0] and lecture_name_urls[0][1]
