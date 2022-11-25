"""
This module provides the app function that executes the cli
"""

from pathlib import Path
from cwm_downloader.exceptions import ElementNotFoundError, IncorrectUrlError
from cwm_downloader.scraper.course_scraper import Course
from cwm_downloader.utils import initialize_session, load_credentials, render_message
from cwm_downloader import __app_name__, __version__
from typing import Optional
import typer

# Initialize the typer app
app = typer.Typer(pretty_exceptions_show_locals=False, no_args_is_help=True)  # Disable showing the locals when an exception occurs.


def _version_callback(value: bool):
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


def _edit_credentials_callback(value: bool):
    """ Launch an editor and edit the credentials.json file. """
    if value:
        # Load the credentials file
        credentials_file = load_credentials()
        render_message("info", f"Credentials File Path: {credentials_file}")
        exit_code = typer.launch(str(credentials_file), wait=True)
        if exit_code == 0:
            # This means every thing is fine and the editor of the os reuturned an exit code of 0
            raise typer.Exit(0)
        else:
            # This means for what ever reason the editor failed to edit the file in that case then inform the user and
            # exit with a code of 1
            render_message('error', 'Failed to edit the file.')
            raise typer.Exit(1)


def check_if_less_than_zero(value: int):
    if value:
        if value <= 0:
            raise typer.BadParameter('Values less than 1 are not allowed')
        return value


def _download(course_obj: Course, section_no: Optional[int], lecture_no: Optional[int], only: bool, base_dir: Path, **download_args):
    """
    Call the perfect download method based on the given section and lecture numbers

    :param course_obj: A course object.
    :param section_no: The index of the section given by the user
    :param lecture_no: The index of the lecture given by the user
    :param only: The only flag given by the user
    :param base_dir: The base directory(path) that is given by the user

    Any other keyword argument will be passed to each download methods. 
    """
    if only:
        # Sample command: cwm-downloader download URL PATH --only
        if not section_no and not lecture_no:
            raise typer.BadParameter('Cannot use --only without a section or lecture')
        # Sample command: cwm-downloader download URL PATH --section INT --lecture INT --only
        if section_no and lecture_no:
            course_obj.download_lecture(base_dir, section_no-1, lecture_no-1, all_sections=None, **download_args)

        # Sample command: cwm-downloader download URL PATH --section INT --only
        elif section_no and not lecture_no:
            course_obj.download_section(base_dir, section_no-1, 0, all_sections=None, **download_args)

        # Sample command: cwm-downloader download URL PATH --lecture 4 --only
        elif lecture_no and not section_no:
            course_obj.download_lecture(base_dir, 0, lecture_no-1, all_sections=None, **download_args)
    else:
        # If section_no and lecture_no are None then change them to 1
        if not section_no:
            section_no = 1
        if not lecture_no:
            lecture_no = 1

        course_obj.download(base_dir, section_no-1, lecture_no-1, **download_args)


@app.callback()
def main(
    version: bool = typer.Option(False, '--version', help="Show the app's version and exit.", callback=_version_callback, is_eager=True),
    edit_credentials: bool = typer.Option(False, '--edit-credentials', help="Edit the credentials.json file and exit.", callback=_edit_credentials_callback)
) -> None:
    """ Download courses from https://codewithmosh.com with ease!. """


@app.command()
def download(
    url: str = typer.Argument(..., help="Any lecture url from the course you want to download."),

    path: Path = typer.Argument(Path('.'), help="The path where the course gets downloaded in. The program creates its own course directory."),

    section_no: Optional[int] = typer.Option(None, '--section', '-s', help="The section from where the download starts.", callback=check_if_less_than_zero),

    lecture_no: Optional[int] = typer.Option(None, '--lecture', '-l', help="The lecture from where the download starts.", callback=check_if_less_than_zero),

    only: bool = typer.Option(False, '--only', help="Download the specified lecture and section only."),

    timeout: int = typer.Option(60, '--timeout', '-T', help="Set the timeout for the connection and the server to respond. (Increase the number if you have a slower connection)."),

    chunk_size: int = typer.Option(4096, help="The chunk that the app downloads at a time when downloading content."),

    noconfirm: bool = typer.Option(False, '--noconfirm', help="Disable the confirmation when overwriting a file.")
):
    try:
        # Initialize a request Session using initialize_session which initializes a session
        # by setting the headers and cookies from the credentials.json file for us.
        with initialize_session() as session:
            course_obj = Course(url, session, timeout)
            _download(course_obj, section_no, lecture_no, only, path, chunk_size=chunk_size, noconfirm=noconfirm)
    # This is an error raised by the url validator found in the base abstract class
    # Scraper in _scraper.py
    except IncorrectUrlError:
        render_message('error', f'Incorrect Url "{url}".')
        render_message('info', f'Use a url with a base of {Course.base_url}')
        raise typer.Exit(1)
    # This is also raised in the abstract base class Scraper and it is raised when an element selctor
    # cannot be found.
    except ElementNotFoundError:
        render_message('error', f'The program could\'nt fetch resources. There might be updates to the site or your subscription has ended. Or you might have an invalid cookies')
        raise typer.Exit(1)
