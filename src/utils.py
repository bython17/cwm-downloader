import json
from time import sleep
from typing import Callable, Dict, Literal
from requests.structures import CaseInsensitiveDict
from requests.utils import cookiejar_from_dict
from requests import Session, exceptions as rqexceptions
from socket import gaierror
from json import loads
from functools import wraps
from rich import print as rprint
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
    with open('credentials.json') as credentials_file:
        return json.loads(credentials_file.read())


def initialize_session():
    session = Session()
    credentials = get_credentials()
    session.cookies = cookiejar_from_dict(credentials['cookies'])
    session.headers = CaseInsensitiveDict(credentials['headers'])
    return session


def render_message(message_type: Literal['info', 'warning', 'error'], message: str, question=False):
    message_color = message_type_color[message_type]
    display_message = f"{message_color}{message_type.upper()} [white]{message}"
    if question:
        return input(f"{display_message}: ")
    rprint(display_message)


def handle_network_errors(func: Callable):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except rqexceptions.SSLError:
            render_message('error', 'SSL error occured retrying...')
            decorated_func(*args, **kwargs)
        except rqexceptions.Timeout:
            render_message('error', 'Server timed out retrying...')
            sleep(5)
            decorated_func(*args, **kwargs)
        except rqexceptions.ConnectionError:
            render_message('error', 'Connenction error. [green]Try Checking your internet connection.')
            sleep(5)
            decorated_func(*args, **kwargs)
        except gaierror as error:
            render_message('error', f'Network error retrying...')
            render_message('error', str(error))
            sleep(5)
            decorated_func(*args, **kwargs)
        except Exception as error:
            render_message('error', 'Unknown error occured retrying...')
            render_message('error', str(error))
            sleep(5)
            decorated_func(*args, **kwargs)
    return decorated_func
