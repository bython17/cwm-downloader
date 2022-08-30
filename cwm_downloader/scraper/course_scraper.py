"""
Provides the Course class which can allow to easily multiple courses.
"""

from pathlib import Path
from cwm_downloader.scraper.lecture_scraper import Lecture
from cwm_downloader.scraper._scraper import Scraper
from urllib.parse import urljoin
from cwm_downloader.utils import render_message, handle_range_error


class Course(Scraper):
    """
    A representation of one course which can gather all sections and lectures
    and that can also download them.
    """

    @handle_range_error
    def download_lecture(self, base_dir: Path, section_no: int, lecture_no: int, all_sections=None, **lecture_download_args):
        """
        Download a lecture using its section number

        :param base_dir: The directory where the lecture will be downloaded
        :param section_no: The index of the section to be downloaded
        :param lecture_no: The index of the lecture to be downloaded
        :param all_sections: A dictionary which maps the sections to a list of their corresponding lectures 

        Since this method uses Lecture.download under the hood the rest of the
        key worded arguments will be used to customize Lecture.download 
        """
        # If all_sections(which is a dictionary that can be get from self.get_all_sections) is not provided then
        # get the all_sections (just to make the app a bit efficient)
        if not all_sections:
            all_sections = self.get_all_sections()
        # Get the name of the section using the seciton number
        section_name_to_download = list(all_sections.keys())[section_no]
        # Get the lecture we want from the all_sections dict
        lecture_to_download = all_sections[section_name_to_download][lecture_no]
        lecture_to_download.download(base_dir, **lecture_download_args)

    @handle_range_error
    def download_section(self, base_dir: Path, section_no: int, lecture_no: int, all_sections=None, **lecture_download_args):
        """
        Download a section using its section number

        :param base_dir: The directory where the section folder will be stored
        :param section_no: The index of the section to be downloaded
        :param lecture_no: The starting index of the lecture to be downloaded
        :param all_sections: A dictionary which maps the sections to a list of their corresponding lectures 

        Since this method uses Lecture.download under the hood the rest of the
        key worded arguments will be used to customize Lecture.download 
        """
        # If all_sections(which is a dictionary that can be get from self.get_all_sections) is not provided then
        # get the all_sections (just to make the app a bit efficient)
        if not all_sections:
            all_sections = self.get_all_sections()

        section_to_download: str = list(all_sections.keys())[section_no]
        render_message('info', f'Starting section [bold blue]{section_to_download}', start='\n', end='\n\n')

        # Create the section directory which houses all lectures
        section_dir = base_dir / section_to_download
        section_dir.mkdir(exist_ok=True)

        # Get the lectures to download in the "section_to_download" key
        lectures_to_download: list[Lecture] = all_sections[section_to_download][lecture_no:]
        for lecture in lectures_to_download:
            lecture.download(section_dir, **lecture_download_args)

    @handle_range_error
    def download(self, base_dir: Path, section_no: int = 0, lecture_no: int = 0,  **section_download_args):
        """
        Download a course starting from a given section number

        :param base_dir: The directory in which the course directory will live in
        :param section_no: The index of the section to start downloading from
        :param lecture_no: The starting index of the lectures found in the first section

        Since this method uses the download_section method under the hood the rest
        of the key worded arguments passed are used to customize download_section.
        """
        # Get the sections and lectures which is a dictionary which maps each section to a list of its lectures
        all_sections = self.get_all_sections()

        # Slice the section from the provided section onwards
        sections_to_download = list(all_sections.keys())[section_no:]

        # Create the course directory inside the base_dir provided.
        course_dir = base_dir / str(self)
        course_dir.mkdir(exist_ok=True)

        # Loop over the enumerations of the selected sections to get the indexes and pass the to download_section which
        # downloads an indivisual section using the seciton number.
        for index, _ in enumerate(sections_to_download):
            # If it is the first section then apply the lecture_no specified
            if index == 0:
                self.download_section(course_dir, index, lecture_no, all_sections, **section_download_args)
                continue
            self.download_section(course_dir, index, 0, all_sections, **section_download_args)
            # We passed all_sections to self.download_section not to call self.get_all_sections everytime

    def get_all_sections(self):
        """
        Returns all the sections mapped with their corresponding lectures.
        """
        section_containers = self.select_element(self.element_selectors.section_containers)
        # We did the above because, if we directly select the section_names or the lecture_anchor_tags we would
        # get a list of all section_names or lecture_anchor_tags which is not wanted. So by selecting the container
        # we can pass the section_container as the source to Scraper.select_element.
        section_lectures = {
            f"{index + 1}- {self.select_element(self.element_selectors.section_names, section_container, single=True).get_text(strip=True)}": [
                # Since we get the relative url of the lectures when using the href attribute of the anchor tags,
                # we can use urljoin which smartly joins the base url with the relative url.
                Lecture(urljoin(self.base_url, lecture.get('href')), self.session, self.timeout) for lecture in self.select_element(self.element_selectors.lecture_anchor_tags, section_container)
            ] for index, section_container in enumerate(section_containers)
        }
        return section_lectures

    def get_name(self):
        """Get the name of the course"""
        course_name = self.select_element(self.element_selectors.course_name, single=True)
        return course_name.get_text(strip=True)
