from pathlib import Path
from bs4 import Tag
from rich.progress import Progress, TaskID
from typing import Dict, Iterable, Literal
from src.scraper._scraper import Scraper
from src.utils import handle_network_errors
from src.scraper.markup_template import create_markup

LectureType = Literal['video', 'text']


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
        print(bare_resource_name)
        lecture_number = self.get_lecture_number() if self.get_lecture_number() is not None else ''
        if bare_resource_name.split('-')[0].isdigit():
            resource_name = '-'.join(bare_resource_name.split('-')[1:]).strip()  # Strip out the number if it exists and remove white spaces
        else:
            resource_name = bare_resource_name.strip()
        return f"{lecture_number}- resource_{resource_name}"

    def download(self, base_dir: Path, progress_bar: Progress, chunk_size: int = 4096):
        lecture_type = self.get_type()
        download_names_urls = self.get_download_names_and_urls()
        if lecture_type == 'text':
            self.__download_text(base_dir)
        if download_names_urls is not None:
            for download_name, download_url in download_names_urls.items():
                if download_name.split('.')[-1] != 'mp4':
                    download_name = self.get_resource_name(download_name)
                self.__download(download_url, base_dir / download_name, progress_bar, chunk_size)

    @handle_network_errors
    def __download(self, url: str, file_path: Path, progress_bar: Progress, chunk_size: int):
        current_task_id: TaskID = progress_bar.add_task('download', filename=file_path, start=False)
        response = self.session.get(url, stream=True, timeout=self.timeout)
        progress_bar.update(current_task_id, total=int(str(response.headers.get('content-length'))))
        progress_bar.start_task(current_task_id)

        with open(file_path) as file:
            for chunk in response.iter_content(chunk_size):
                file.write(chunk)
                progress_bar.update(current_task_id, advance=chunk_size)

    def __download_text(self, base_dir: Path):
        lecture_name = self.get_name()
        lecture_main_container = self.get_text_lecture()
        lecture_markup = create_markup(lecture_name, lecture_main_container)
        with open(base_dir / f"{lecture_name}.html", 'w') as html_file:
            html_file.write(lecture_markup)

    def get_name(self) -> str:
        lecture_name = self.select_element(self.element_selectors.lecture_name, single=True)
        return lecture_name.get_text(strip=True)

    def get_type(self) -> LectureType:
        lecture_icon = self.select_element(self.element_selectors.lecture_icon, single=True).get('xlink:href')
        if lecture_icon == "#icon__Video":
            return 'video'
        else:
            return 'text'
