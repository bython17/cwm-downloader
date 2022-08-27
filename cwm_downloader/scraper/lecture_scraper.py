from pathlib import Path
from bs4 import Tag
from rich.progress import Progress, TaskID
from typing import Dict, Iterable, Literal
from cwm_downloader.scraper._scraper import Scraper
from cwm_downloader.utils import get_progress_bar, handle_keyboard_interrupt_for_files, handle_network_errors, render_message
from cwm_downloader.scraper.markup_template import create_markup

LectureType = Literal['video', 'text']
FORBIDDEN_CHARACTERS = r'<>:"/\|?*'


class Lecture(Scraper):
    def get_download_names_and_urls(self) -> Dict[str, str] | None:
        download_tags = self.select_element(self.element_selectors.download_tags, raise_if_not_found=False)
        if download_tags is None:
            return None
        return {tag.get('data-x-origin-download-name'): tag.get('href') for tag in download_tags}

    def decompose_elements(self, element_selectors: Iterable[str], source: Tag) -> None:
        for element_selector in element_selectors:
            decomposable_element = source.select_one(element_selector)
            if decomposable_element is not None:
                decomposable_element.decompose()

    def get_text_lecture(self) -> str:
        main_container = self.select_element(self.element_selectors.main_container_div, single=True)
        self.select_element(self.element_selectors.attribute_cleared_meta_tag, main_container, single=True).attrs = {}
        self.decompose_elements(self.element_selectors.decomposable_elements.value, main_container)
        return main_container.prettify()

    def get_lecture_number(self) -> str | None:
        lecture_name = self.get_name()
        lecture_name_number = lecture_name.split('-')
        if len(lecture_name_number) < 1 or not lecture_name_number[0].strip().isdigit():
            return None
        return lecture_name_number[0]

    def get_resource_name(self, bare_resource_name: str) -> str:
        lecture_number = self.get_lecture_number() if self.get_lecture_number() is not None else ''
        if bare_resource_name.split('-')[0].isdigit():
            resource_name = '-'.join(bare_resource_name.split('-')[1:]).strip()  # Strip out the number if it exists and remove white spaces
        else:
            resource_name = bare_resource_name.strip()
        return f"{lecture_number}- resource_{resource_name}"

    @staticmethod
    def sterilize_filename(file_name: str):
        for character in file_name:
            if character in FORBIDDEN_CHARACTERS:
                file_name = file_name.replace(character, '')
        file_name_list = [file_name_section.strip() for file_name_section in file_name.split('.') if file_name_section.strip() != '']
        return '.'.join(file_name_list)

    @staticmethod
    def should_overwrite(file_path: Path):
        if file_path.exists():
            return render_message('warning', f'File named "{file_path.name}" exists. Shall I overwrite the file', question=True)
        return True

    def download(self, base_dir: Path,  chunk_size: int = 4096):
        lecture_type = self.get_type()
        download_names_urls = self.get_download_names_and_urls()
        if lecture_type == 'text':
            filename = self.sterilize_filename(f"{str(self)}.html")
            file_path = base_dir / filename
            if self.should_overwrite(file_path):
                with get_progress_bar() as progress_bar:
                    current_task_id: TaskID = progress_bar.add_task('download', start=False, filename=str(self))
                    self.__download_text(file_path, progress_bar, current_task_id)
        if download_names_urls is not None:
            for download_name, download_url in download_names_urls.items():
                filename = self.sterilize_filename(download_name)
                if filename.split('.')[-1] != 'mp4':
                    filename = self.get_resource_name(filename)
                file_path = base_dir / filename
                if self.should_overwrite(file_path):
                    with get_progress_bar() as progress_bar:
                        current_task_id = progress_bar.add_task('download', filename=file_path.stem, start=False)
                        self.__download(download_url, file_path, progress_bar, current_task_id, chunk_size)
        elif download_names_urls is None and lecture_type != 'text':
            render_message('warning', f'Skipping, Nothing to download in lecture "{str(self)}".')

    @handle_network_errors
    @handle_keyboard_interrupt_for_files
    def __download(self, url: str, file_path: Path, progress_bar: Progress, current_task_id: TaskID, chunk_size: int):
        response = self.session.get(url, stream=True, timeout=self.timeout)
        progress_bar.reset(current_task_id, start=False)
        progress_bar.update(current_task_id, total=int(str(response.headers.get('content-length'))))
        progress_bar.start_task(current_task_id)

        with file_path.open('wb') as file:
            for chunk in response.iter_content(chunk_size):
                file.write(chunk)
                progress_bar.update(current_task_id, advance=chunk_size)

    @handle_keyboard_interrupt_for_files
    def __download_text(self, file_path: Path, progress_bar: Progress, current_task_id: TaskID):
        progress_bar.start_task(current_task_id)
        lecture_main_container = self.get_text_lecture()
        lecture_markup = create_markup(str(self), lecture_main_container)
        with file_path.open('w') as html_file:
            html_file.write(lecture_markup)
        progress_bar.update(current_task_id, completed=100)

    def get_name(self) -> str:
        lecture_name = self.select_element(self.element_selectors.lecture_name, single=True)
        return lecture_name.get_text(strip=True)

    def get_type(self) -> LectureType:
        lecture_icon = self.select_element(self.element_selectors.lecture_icon, single=True).get('xlink:href')
        if lecture_icon == "#icon__Video":
            return 'video'
        else:
            return 'text'
