from pathlib import Path
from cwm_downloader.exceptions import ElementNotFoundError, IncorrectUrlError
from cwm_downloader.scraper.course_scraper import Course
from cwm_downloader.utils import initialize_session, render_message
from requests import Session
import typer


class ArgumentParser:
    def __init__(self, session: Session):
        self.session = session
        typer.run(self.main)

    def section_or_lecture_parser(self, value: int, only=False):
        if value <= 0:
            raise typer.BadParameter(f'{value}. The value should be greater than 0.')
        if not only:
            return [value, 'end']
        return [value, value]

    def is_single_lecture(self, sections: list, lectures: list):
        if len(sections) == 1 and len(lectures) == 1:
            return True
        return False

    def main(
        self,
        url: str = typer.Argument(..., help="Any lecture url from the course you want to download."),

        path: Path = typer.Argument(Path('.'), help="The path where the course gets downloaded in. The program creates its own course directory."),

        section: int = typer.Option(1, '--section', '-s', help="The section from where the download starts."),

        lecture: int = typer.Option(1, '--lecture', '-l', help="The lecture from where the download starts."),

        only: bool = typer.Option(False, '--only', help="Download the specified lecture and section only."),

        timeout: int = typer.Option(60, '--timeout', '-T', help="Set the timeout for the connection and the server to respond. (Increase the number if you have a slower connection)."),

        chunk_size: int = typer.Option(4096, help="The chunk that the app downloads at a time when downloading content."),

        noconfirm: bool = typer.Option(False, '--noconfirm', help="Disable the confirmation when overwriting a file.")
    ):
        formatted_section = self.section_or_lecture_parser(section, only)
        formatted_lecture = self.section_or_lecture_parser(lecture, only)

        try:
            course_obj = Course(url, self.session, timeout)
            course_obj.download(path, formatted_section, formatted_lecture, chunk_size, noconfirm)
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
