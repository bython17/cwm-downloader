"""
This modules provides a Lecture class that can download a lecture
using its url.
"""
from pathlib import Path
from bs4 import Tag
from rich.progress import Progress, TaskID
from typing import Dict, Iterable, Literal
from cwm_downloader.scraper._scraper import Scraper
from cwm_downloader.utils import get_progress_bar, handle_keyboard_interrupt_for_files, handle_network_errors, render_message, sterialize_file_or_folder
from cwm_downloader.scraper.markup_template import create_markup

# These are two possible types of a lecture that are
# either a video type or a text type.
LectureType = Literal['video', 'text']

class Lecture(Scraper):
    """
    Download any lecture with its resources (Download any thing in the lecture page that has an anchor tag
    with a download class).
    """

    def get_download_names_and_urls(self) -> Dict[str|None, str] | None:
        """ Get all downloadable urls with their filenames as a dictionary. """
        # Select all elements with the download_tags element selector
        # Recognize that raise_if_not_found is False that makes it so even if
        # There is no download link found the ElementNotFoundError error won't
        # be raised.
        download_tags = self.select_element(self.element_selectors.download_tags, raise_if_not_found=False)
        if download_tags is None:
            return None
        result = {}
        for tag in download_tags:
            orig_name = tag.get("data-x-origin-download-name")
            url = tag.get("href")
            if "://" not in url:
                # This means that the url is a relative url so we need to join it with the base url
                url = self.base_url + url
            result[orig_name] = url
            # having result[None] will result in only one entry for all links without data-x-origin-download-name
        return result

    def decompose_elements(self, element_selectors: Iterable[str], source: Tag) -> None:
        """ 
        Delete all elements specified by the element_selectors in the source.
        Element's that don't exist will be ignored.

        :param element_selectors: The element's to be removed from the source
        :param source: A Tag that contains the removable elements
        """
        for element_selector in element_selectors:
            decomposable_element = source.select_one(element_selector)
            # If the element is None(doesn't exist) then skip it
            if decomposable_element is not None:
                # The decompose method will wipe out the element itself and
                # all its children.
                decomposable_element.decompose()

    def get_text_lecture(self) -> str:
        """ 
        Returns a string of a text lecture html with unecessary tags and attrs removed. 

        And remove the attributes found on the meta tag to clean things up.
        """
        main_container = self.select_element(self.element_selectors.main_container_div, single=True)
        # To remove the attributes just set the attrs attribute of the tag to an empty dict
        self.select_element(self.element_selectors.attribute_cleared_meta_tag, main_container, single=True).attrs = {}
        # We decomoposed all the decomposable elements which are unecessary
        self.decompose_elements(self.element_selectors.decomposable_elements.value, main_container)
        return main_container.prettify()

    def get_lecture_number(self) -> str | None:
        """ Get the lecture number if it exists if it doesn't return None"""
        lecture_name = self.get_name()
        # Split the lecture name with a "-"" since thats what the lectures separate their numbers in
        lecture_name_number = lecture_name.split('-')
        if len(lecture_name_number) < 1 or not lecture_name_number[0].strip().isdigit():
            # This means that either there is no "-" sign which probably means no number
            # or the first index is not a digit
            return None
        return lecture_name_number[0]

    def get_resource_name(self, bare_resource_name: str) -> str:
        """
        Get the name of a resource(insert a "resource_" to the name)

        :param bare_resource_name: The name of the resource that is returned from self.get_download_names_and_urls
        """
        # Set a lecture number only if it is not None else use an empty string
        lecture_number = self.get_lecture_number() if self.get_lecture_number() is not None else ''
        # If the first element before the "-" is a digit then
        if bare_resource_name.split('-')[0].isdigit():
            # Remove every white space and also remove the number at the first of the name
            resource_name = '-'.join(bare_resource_name.split('-')[1:]).strip()
        else:
            resource_name = bare_resource_name.strip()
        # if we have no extension, assume it's a video in mp4 format
        if "." not in resource_name:
            resource_name += ".mp4"
        try:
            # Try to format the lecture number to a 2 digit number
            lecture_number = f"{int(lecture_number):02d}"
        except ValueError:
            pass  # not interested, if it's not a number, keep the string as it is
        return f"{lecture_number}-resource_{resource_name}"

    @staticmethod
    def should_overwrite(file_path: Path, noconfirm=False):
        """
        Ask to overwrite the file_path if it exists and noconfirm is false

        :param file_path: The file path to check for
        :param noconfirm: to forcibly disable to ask for the user input and just return True
        """
        if noconfirm:
            return True
        if file_path.exists():
            return render_message('warning', f'File named "{file_path.name}" exists. Shall I overwrite the file', question=True)
        return True

    def download(self, base_dir: Path,  chunk_size: int = 4096, noconfirm=False):
        """
        Downloads a lecture with all its resources and any other downloadable things

        :param base_dir: Where to store the downloaded content
        :param chunk_size: How much bytes to wait before writing it to a file.
        :param noconfirm: If the user shouldn't be asked for confirmation about overwriting a file.
        """

        lecture_type = self.get_type()
        download_names_urls = self.get_download_names_and_urls()
        if lecture_type == 'text':
            filename = sterialize_file_or_folder(f"{str(self)}.html")
            file_path = base_dir / filename
            if self.should_overwrite(file_path, noconfirm):
                # We initialize progress bars here because if it was initialized at the top level
                # Confirm.ask(which uses live and itself is used by self.should_overwrite) will not work
                # according to rich
                with get_progress_bar() as progress_bar:
                    # initializing the progress task here helps us so that when the download is retried
                    # another thask wont be instatiated.
                    current_task_id: TaskID = progress_bar.add_task('download', start=False, filename=str(self))
                    self.__download_text(file_path, progress_bar, current_task_id)
        if download_names_urls is not None:
            for download_name, download_url in download_names_urls.items():
                if download_name is None:
                    # get the web page title and use it as the filename
                    download_name = self.get_name()
                    filename = sterialize_file_or_folder(
                        self.get_resource_name(download_name)
                    )
                else:
                    filename = sterialize_file_or_folder(download_name)
                if filename.split('.')[-1] != 'mp4':
                    # This means that the downloadable thing is a resource so
                    # we use the self.get_resource_name to get the resource name
                    filename = self.get_resource_name(filename)
                file_path = base_dir / filename
                if self.should_overwrite(file_path, noconfirm):
                    with get_progress_bar() as progress_bar:
                        # The samething as the text lecture here
                        current_task_id = progress_bar.add_task('download', filename=file_path.stem, start=False)
                        self.__download(download_url, file_path, progress_bar, current_task_id, chunk_size)
        elif download_names_urls is None and lecture_type != 'text':
            # This means that there are no download urls and the lecture is a video
            # In this case the only option we have is to inform the user and skip this lecture.
            render_message('warning', f'Skipping, Nothing to download in lecture "{str(self)}".')

    @handle_network_errors
    @handle_keyboard_interrupt_for_files
    def __download(self, url: str, file_path: Path, progress_bar: Progress, current_task_id: TaskID, chunk_size: int):
        """
        Download any downloadble url and show a progress bar while also handling network and keyboard interrupt errors
        that occur.

        :param url: The downloadable url
        :param file_path: Where to store the final file
        :param progress_bar: A rich.Progress object used to update the current progress bar task
        :param current_task_id: The id of the task to use when downloading
        :parm chunk_size: How much bytes to wait before writing it to a file.
        """
        # All error that happen here are hanled by the decorators so no worries 😁
        response = self.session.get(url, stream=True, timeout=self.timeout)
        # Reset the progress bar because the decorator will call this function again and if it
        # is not reset the progress bar will continue from where it left of but the download resets
        # which is wierd! right?
        progress_bar.reset(current_task_id, start=False)
        progress_bar.update(current_task_id, total=int(str(response.headers.get('content-length'))))
        progress_bar.start_task(current_task_id)

        with file_path.open('wb') as file:
            for chunk in response.iter_content(chunk_size):
                file.write(chunk)
                progress_bar.update(current_task_id, advance=chunk_size)

    @handle_keyboard_interrupt_for_files
    def __download_text(self, file_path: Path, progress_bar: Progress, current_task_id: TaskID):
        """
        Download(modify and save to storage) any text lecture. This method doesn't really download
        anything since everything it needs is already download when the soup is made so we use that instead
        and save it to the file system.

        :param file_path: Where to store the final file
        :param progress_bar: A rich.Progress object used to update the current progress bar task
        :param current_task_id: The id of the task to use when saving
        """
        progress_bar.start_task(current_task_id)
        # Get all the html necessary for creating the file
        lecture_main_container = self.get_text_lecture()
        # Inject styles and make a proper html document using create_markup
        lecture_markup = create_markup(str(self), lecture_main_container)
        with file_path.open('w') as html_file:
            html_file.write(lecture_markup)
        progress_bar.update(current_task_id, completed=100)

    def get_name(self) -> str:
        """ Get the name of the lecture"""
        lecture_name = self.select_element(self.element_selectors.lecture_name, single=True)
        return lecture_name.get_text(strip=True)

    def get_type(self) -> LectureType:
        """ Get the type of the lecture which is a type of LectureType"""
        lecture_icon = self.select_element(self.element_selectors.lecture_icon, single=True).get('xlink:href')
        if lecture_icon == "#icon__Video":
            return 'video'
        else:
            return 'text'
