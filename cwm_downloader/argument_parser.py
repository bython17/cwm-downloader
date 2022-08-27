from pathlib import Path
from typing import Union
from cwm_downloader.exceptions import ElementNotFoundError, IncorrectUrlError
from cwm_downloader.scraper.course_scraper import Course
from cwm_downloader.utils import initialize_session, render_message
from requests import Session
import typer


class ArgumentParser:
    def __init__(self, session: Session):
        self.session = session
        typer.run(self.main)

    def section_or_lecture_parser(self, value: str, onwards=False):
        indices = value.split('-')
        formated_indices: list[Union[int, str]] = []

        if onwards and len(indices) > 1:
            raise typer.BadParameter(f'"--onwards" can only be used with a single lecture and section')

        elif onwards:
            return [value, 'end']

        if len(indices) > 2:
            raise typer.BadParameter(f'"{value}" is not allowed.')

        for index in indices:
            if index.lower() == 'all':
                formated_indices = ['start', 'end']
                break
            elif index.lower() == 'start' or index.lower() == 'end':
                formated_indices.append(index)
            elif index.isdigit():
                formated_indices.append(int(index))
            else:
                raise typer.BadParameter(f'"{index}" in "{value}" is not allowed.')

        return formated_indices

    def is_single_lecture(self, sections: list, lectures: list):
        if len(sections) == 1 and len(lectures) == 1:
            return True
        return False

    def main(
        self,
        url: str = typer.Argument(..., help="Any lecture url from the course you want to download."),

        path: Path = typer.Argument(Path('.'), help="The path where the course gets downloaded in. The program creates its own course directory."),

        section: str = typer.Option('start', '--section', '-s', help="The section from where the download starts."),

        lecture: str = typer.Option('end', '--lecture', '-l', help="The section from where the download starts."),

        onwards: bool = typer.Option(False, help="Download all lectures and sections after the specified section and lecture."),

        timeout: int = typer.Option(60, '--timeout', '-T', help="Set the timeout for the connection and the server to respond. (Increase the number if you have a slower connection)."),

        chunk_size: int = typer.Option(4096, help="The chunk that the app downloads at a time when downloading content.")
    ):
        formatted_section = self.section_or_lecture_parser(section, onwards)
        formatted_lecture = self.section_or_lecture_parser(lecture, onwards)

        try:
            course_obj = Course(url, self.session, timeout)
            course_obj.download(path, formatted_section, formatted_lecture, chunk_size)
        except IncorrectUrlError:
            render_message('error', f'Incorrect Url "{url}".')
            render_message('info', f'Use a url with a base of {Course.base_url}')
            typer.Exit(1)
        except ElementNotFoundError:
            render_message('error', f'The program could\'nt fetch resources. There might be updates to the site or your subscription has ended. Or you might have an invalid cookies')
            typer.Exit(1)


if __name__ == "__main__":
    with initialize_session() as session:
        ArgumentParser(session)
