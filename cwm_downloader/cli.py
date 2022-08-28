from pathlib import Path
from cwm_downloader.exceptions import ElementNotFoundError, IncorrectUrlError
from cwm_downloader.scraper.course_scraper import Course
from cwm_downloader.utils import initialize_session, render_message, create_credentials
from sys import exit
import typer

app = typer.Typer(name="cwm-downloader", no_args_is_help=False, pretty_exceptions_show_locals=False)


def section_or_lecture_parser(value: int, only=False):
    if value <= 0:
        raise typer.BadParameter(f'{value}. The value should be greater than 0.')
    if not only:
        return [value, 'end']
    return [value, value]


def is_single_lecture(sections: list, lectures: list):
    if len(sections) == 1 and len(lectures) == 1:
        return True
    return False


def manage_credentials(credentials_file: Path, edit_credentials: bool):
    if not credentials_file.is_file():
        create_credentials(credentials_file)

    if edit_credentials:
        exit_code = typer.launch(str(credentials_file), wait=True)
        if exit_code == 0:
            exit(0)
        else:
            render_message('error', 'Failed to edit the file.')
            exit(1)


def create_safe_base_app_dir():
    app_base_dir = Path(typer.get_app_dir('cwm-downloader'))
    if not app_base_dir.exists():
        app_base_dir.mkdir(parents=True)
    return app_base_dir


@app.command()
def main(
    url: str = typer.Argument(..., help="Any lecture url from the course you want to download."),

    path: Path = typer.Argument(Path('.'), help="The path where the course gets downloaded in. The program creates its own course directory."),

    section: int = typer.Option(1, '--section', '-s', help="The section from where the download starts."),

    lecture: int = typer.Option(1, '--lecture', '-l', help="The lecture from where the download starts."),

    only: bool = typer.Option(False, '--only', help="Download the specified lecture and section only."),

    timeout: int = typer.Option(60, '--timeout', '-T', help="Set the timeout for the connection and the server to respond. (Increase the number if you have a slower connection)."),

    chunk_size: int = typer.Option(4096, help="The chunk that the app downloads at a time when downloading content."),

    noconfirm: bool = typer.Option(False, '--noconfirm', help="Disable the confirmation when overwriting a file."),

    edit_credentials: bool = typer.Option(False, '--edit-credentials', help="Edit the credentials.json file and exit.", is_eager=True)
):
    app_base_dir = create_safe_base_app_dir()
    credentials_file = app_base_dir / 'credentials.json'

    manage_credentials(credentials_file, edit_credentials)

    formatted_section = section_or_lecture_parser(section, only)
    formatted_lecture = section_or_lecture_parser(lecture, only)

    try:
        with initialize_session(credentials_file) as session:
            course_obj = Course(url, session, timeout)
            course_obj.download(path, formatted_section, formatted_lecture, chunk_size, noconfirm)
    except IncorrectUrlError:
        render_message('error', f'Incorrect Url "{url}".')
        render_message('info', f'Use a url with a base of {Course.base_url}')
        exit(1)
    except ElementNotFoundError:
        render_message('error', f'The program could\'nt fetch resources. There might be updates to the site or your subscription has ended. Or you might have an invalid cookies')
        exit(1)
