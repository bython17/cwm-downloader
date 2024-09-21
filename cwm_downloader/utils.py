""" 
This module is a helper to all modules in this project it contains alot of useful functions
for the scrapers and the cli
"""

import json
from time import sleep
import typer
from typing import Callable, Dict, Literal, Optional
from cwm_downloader.exceptions import InvalidCredentialsError
from cwm_downloader import __app_name__
from requests.structures import CaseInsensitiveDict
from requests.utils import cookiejar_from_dict
from requests import Session, exceptions as rqexceptions
from socket import gaierror
from pathlib import Path, PurePath
from functools import wraps
from rich import print as rprint
from rich.prompt import Confirm
from rich.status import Status
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

# Mapping the the error types with their styles
message_type_color = {
    'info': '[bold green]',
    'warning': '[bold yellow]',
    'error': '[bold red]'
}

# Just creating a type alias for the credentials type
# Since its a bit complicated and mistakes could be
# easily made when typing it again 😁
credentials_type = Dict[str, Dict[str, str]]

# This is the most basic dict form of the
# credentials.json file
credentials_template: credentials_type = {
    'headers': {},
    'cookies': {},
}


def get_safe_base_app_dir():
    """ Get the app's config directory safely (create it even if it doesn't exist). """
    # Resolving the directories helps for symlinks and otherthings
    # basically it allows us to get the absolute path of the application.
    app_base_dir = Path(typer.get_app_dir(__app_name__)).resolve()
    if not app_base_dir.exists():
        app_base_dir.mkdir(parents=True)
    return app_base_dir


# Get the app directory using get_safe_app_dir
# which will create the dir if it doesn't exist
APP_DIR = get_safe_base_app_dir()
# And set the credentials.json path
# currently we don't really care if it exists or not
# we are going to validate that in load_credentials
CREDENTIALS_FILE = APP_DIR / 'credentials.json'

# Forbidden file and foldre name characters
# mainly for windows but also for linux.
FORBIDDEN_CHARACTERS = r'<>:"/\|?*'


def load_credentials():
    """ Return an existing credentials_file path"""
    # First check if the CREDENTIALS_FILE doesn't exist and
    # if it doesn't then create one with create_credentials
    if not CREDENTIALS_FILE.is_file():
        create_credentials()
    return CREDENTIALS_FILE


def create_credentials():
    """
    Create a credentials file with a predefined template

    :param credentials_file: The path of the credentials file to create
    """
    credentials_data = json.dumps(credentials_template)
    # First create the credentials file
    # before writing in to it
    CREDENTIALS_FILE.touch(exist_ok=True)
    CREDENTIALS_FILE.write_text(credentials_data)


def get_credentials() -> credentials_type:
    """
    Get the credentials and load it to a python dict and if it isn't valid
    raise an InvalidCredentialsError

    :param credentials_file: The file to open and read for the credentials
    """
    # Load the credentials.json file
    credentials_file = load_credentials()

    credentials_dict = json.loads(credentials_file.read_text())
    # Check if the headers and cookies are not inside the dictionary
    # and raise an error if they are not.
    if 'headers' not in credentials_dict or 'cookies' not in credentials_dict:
        raise InvalidCredentialsError('The contents in credentials.json are invalid.')
    # remove Accept-Encoding from the headers to remove compression
    if "Accept-Encoding" in credentials_dict["headers"]:
        del credentials_dict["headers"]["Accept-Encoding"]
    return credentials_dict


def get_progress_bar():
    """ Generate a progress bar with a predefined config """
    return Progress(
        TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
        BarColumn(bar_width=None),
        "[progress.percentage]{task.percentage:>3.1f}%",
        "•",
        DownloadColumn(),
        "•",
        TransferSpeedColumn(),
        "•",
        TimeRemainingColumn(),
    )


def get_status(message: str):
    return Status(message)


def render_message(message_type: Literal['info', 'warning', 'error'], message: str, question=False, end: str = '\n', start: str = '', styles: str = '[default white]'):
    """
    Display a message to the terminal and customize it with styles and colors.

    :param message_type: The type of the message [info, warning or error]
    :param message: The message to display to the user
    :param question: If true rather than just displaying a message change that message to
    a rich.Confirm and return the result
    :param start: Any text to put before the whole message
    :param end: Any text to put after the whole message
    :param styles: A rich markup used to style the message
    """
    message_color = message_type_color[message_type]
    # Create the message in a format of
    # MESSAGE_TYPE MESSAGE
    display_message = f"{message_color}{message_type.upper()} {styles}{message}[/]"
    if question:
        # This means that the quesiton param is True and that means
        # We should return the rich.Confirm
        return Confirm.ask(f"{styles}{display_message}", default=False)
    else:
        # This means that it isn't a question so just display the
        # message using rich.print which supports colors and rich
        # markup.
        rprint(f"{start}{display_message}", end=end)


def handle_range_error(func: Callable):
    """ 
    A decorator for handling range related errors. 
    When the error occurs it's simply gonne inform the user about it and then exit.
    """
    @wraps(func)
    def decorated_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            render_message('error', 'The specified section or lecture doesn\'t exist.')
            raise typer.Exit(1)
    return decorated_func


def handle_invalid_credentials(func: Callable):
    """ 
    A decorator for handling the InvalidCredentialsError error. When the error occurs
    it's simply gonne inform the user about it and then exit.
    """
    @wraps(func)
    def decorated_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InvalidCredentialsError:
            render_message('error', f'The content inside credentials.json is not valid. Please add the appropriate headers and cookies.')
            render_message('info', 'Use the --edit-credentials flag to edit the credentials.')
            raise typer.Exit(1)
    return decorated_func


def handle_keyboard_interrupt_for_files(func: Callable):
    """ 
    A decorator for hanling the KeyboardInterrupt error for file inteructions 
    when the exception occurs it's going to delete the file and exit the app.
    """
    @wraps(func)
    def decorated_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            file_path: Optional[Path] = None
            for arg in args:
                if isinstance(arg, PurePath):
                    file_path = arg
                    break
            if file_path:
                render_message('warning', 'Process interupted. cleaning up...')
                file_path.unlink(missing_ok=True)
                render_message('info', 'Cleanup was succesfull')
                raise typer.Exit(0)
    return decorated_func


def handle_network_errors(func: Callable):
    """ 
    A decorator to handle network errors for request downloads.
    if any error occurs it is going to recurse the inner decorated_func
    until the it finishes. And it is going to log the errors when doing so.
    """
    @wraps(func)
    def decorated_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except rqexceptions.SSLError:
            render_message('error', 'SSL error occured retrying...')
            return decorated_func(*args, **kwargs)
        except rqexceptions.Timeout:
            render_message('error', 'Server timed out retrying...')
            sleep(5)
            return decorated_func(*args, **kwargs)
        except rqexceptions.ConnectionError:
            render_message('error', 'Connection error. [green]Try Checking your internet connection.')
            sleep(5)
            return decorated_func(*args, **kwargs)
        except gaierror as error:
            render_message('error', f'Network error retrying...')
            render_message('error', str(error))
            sleep(5)
            return decorated_func(*args, **kwargs)
        except typer.Exit as err:
            raise typer.Exit(err.exit_code)
        except Exception as error:
            render_message('error', 'Unknown error occured retrying...')
            render_message('error', str(error))
            sleep(5)
            return decorated_func(*args, **kwargs)
    return decorated_func


def sterialize_file_or_folder(file_name: str):
    """ 
    Sterialize a file names by striping out all the FORBIDEN_CHARACHTERS and keeping
    other filename rules.

    :param file_name: The name of the file to be sterialized
    """
    for character in file_name:
        if character in FORBIDDEN_CHARACTERS:
            file_name = file_name.replace(character, '')
    # Split the file name by the . sybmbol (which results in a filename and an extension most of the time) and then filter
    # the list for empty strings(this means that the those were extra "." left) and strip each of the rest.
    file_name_list = [file_name_section.strip() for file_name_section in file_name.split('.') if file_name_section.strip() != '']
    return '.'.join(file_name_list)


@handle_invalid_credentials
def initialize_session():
    """
    Initialize a session with the headers and cookies that are found
    from the credentials_file.

    :param credentials_file: The file to read the headers and cookies.
    """
    session = Session()
    credentials = get_credentials()
    session.cookies = cookiejar_from_dict(credentials['cookies'])
    session.headers = CaseInsensitiveDict(credentials['headers'])
    return session
