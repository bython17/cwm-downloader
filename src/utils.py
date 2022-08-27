import json
from time import sleep
from typing import Callable, Dict, Literal
from sys import exit
from src.exceptions import CredentialsNotFoundError, InvalidCredentialsError
from requests.structures import CaseInsensitiveDict
from requests.utils import cookiejar_from_dict
from requests import Session, exceptions as rqexceptions
from socket import gaierror
from pathlib import Path
from functools import wraps
from rich import print as rprint
from rich.prompt import Confirm
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)


def get_progress_bar():
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


message_type_color = {
    'info': '[bold green]',
    'warning': '[bold yellow]',
    'error': '[bold red]'
}


def get_credentials() -> Dict[str, Dict[str, str]]:
    credentials_path = Path('./credentials.json')
    if credentials_path.is_file():
        credentials_dict = json.loads(credentials_path.read_text())
        if 'headers' not in credentials_dict or 'cookies' not in credentials_dict:
            raise InvalidCredentialsError('The contents in credentials.json are invalid.')
        return credentials_dict
    else:
        raise CredentialsNotFoundError('The file credentials.json doesn\'t exist.')


def render_message(message_type: Literal['info', 'warning', 'error'], message: str, question=False, end: str = '\n', start: str = '', styles: str = '[default white]'):
    message_color = message_type_color[message_type]
    display_message = f"{message_color}{message_type.upper()} {styles}{message}[/]"
    if question:
        return Confirm.ask(f"{styles}{display_message}", default=False)
    else:
        rprint(f"{start}{display_message}", end=end)


def handle_credentials_not_found_error(func: Callable):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CredentialsNotFoundError:
            render_message('error', f'The file credentials.json could not be found')
            render_message('info', f'Create a credentials.json file in your current directory and add appropriate cookies and headers.')
            exit(1)
        except InvalidCredentialsError:
            render_message('error', f'The content inside credentials.json is not valid. Please add the appropriate headers and cookies.')
            exit(1)
    return decorated_func


def handle_keyboard_interrupt_for_files(func: Callable):
    @wraps(func)
    def decorated_func(file: Path, *args, **kwargs):
        try:
            return func(file, *args, **kwargs)
        except KeyboardInterrupt:
            render_message('warning', 'Process interupted. cleaning up...')
            file.unlink(missing_ok=True)
            render_message('info', 'Cleanup was succesfull')
            exit(0)


def handle_network_errors(func: Callable):
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
        except Exception as error:
            render_message('error', 'Unknown error occured retrying...')
            render_message('error', str(error))
            sleep(5)
            return decorated_func(*args, **kwargs)
    return decorated_func


@handle_credentials_not_found_error
def initialize_session():
    session = Session()
    credentials = get_credentials()
    session.cookies = cookiejar_from_dict(credentials['cookies'])
    session.headers = CaseInsensitiveDict(credentials['headers'])
    return session
