from enum import Enum


class ElementSelectors(Enum):
    course_name = [
        # "#__next div div div.jsx-1640592643.wrap h1",
        "body section div.course-sidebar h2"
    ]
    section_containers = [
        # "body section div.course-mainbar div.row div",
        "div.course-sidebar div.row.lecture-sidebar div.course-section"
    ]
    section_names = [
        "div.course-sidebar div.row.lecture-sidebar div.course-section div.section-title",
        # "body section div.course-mainbar div.row div div"
    ]
    lecture_name = ["#lecture_heading"]
    lecture_icon = ['#lecture_heading svg use']
    lecture_anchor_tags = [
        "div.course-sidebar div.row.lecture-sidebar div.course-section a.item",
        "body section div.course-mainbar div.row div ul li a",
    ]
    download_tags = ["a.download"]
    main_container_div = ["body section div.course-mainbar.lecture-content.full-width-content.enforce-maximum-content-width"]
    decomposable_elements = ['a.btn.complete.lecture-complete', '#empty_box', 'div.attachment-data', 'div.row attachment-pdf-embed']
    attribute_cleared_meta_tag = ['#lecture-completion-data']


print(ElementSelectors.section_containers.value)
