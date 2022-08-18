from enum import Enum


class ElementSelectors(Enum):
    course_name = [
        "#__next > div > div > div.jsx-1640592643.wrap > h1",
        "body > section > div.course-sidebar > h2"
    ]
    section_names = [
        "#__next > div > div > div.jsx-4204861187.columns > div:nth-child(1) > div.slim-selection > div.jsx-4255369697.section-header > div:nth-child(1) > h2",
        "body > section > div.course-mainbar > div.row > div > div"
    ]
    lecture_names = [
        "#__next > div > div > div.jsx-4204861187.columns > div:nth-child(1) > div.slim-selection > div.jsx-3137867545.lectures > div.jsx-4132056062.bar > a.jsx-4132056062.text > h3",
        "body > section > div.course-mainbar > div.row > div > ul > li > a > div > span.lecture-name"
    ]
    lecture_anchor_tags = [
        "#__next > div > div > div.jsx-4204861187.columns > div:nth-child(1) > div.slim-selection > div.jsx-3137867545.lectures > div.jsx-4132056062.bar > a.jsx-4132056062.text",
        "body > section > div.course-mainbar > div.row > div > ul > li > a"
    ]
