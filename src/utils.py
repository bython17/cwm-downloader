from time import sleep
from typing import Callable, Literal
from requests.structures import CaseInsensitiveDict
from requests.utils import cookiejar_from_dict
from requests import Session, exceptions as rqexceptions
from socket import gaierror
from json import loads
from functools import wraps
from src.credentials import headers, cookies
from rich import print as rprint

message_type_color = {
    'info': '[bold green]',
    'warning': '[bold yellow]',
    'error': '[bold red]'
}


def initialize_session():
    session = Session()
    session.cookies = cookiejar_from_dict(cookies)
    session.headers = CaseInsensitiveDict(headers)
    return session


def get_element_selectors(json_filepath: str = './scraper') -> dict[str, list[str]]:
    with open(f"{json_filepath}/element_selectors.json", 'r') as file:
        return loads(file.read())


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
            func(*args, **kwargs)
        except rqexceptions.Timeout:
            render_message('error', 'Server timed out retrying...')
            sleep(5)
            func(*args, **kwargs)
        except rqexceptions.ConnectionError:
            render_message('error', 'Connenction error. [green]Try Checking your internet connection.')
            sleep(5)
            func(*args, **kwargs)
        except gaierror as error:
            render_message('error', f'Network error retrying...')
            render_message('error', str(error))
            sleep(5)
            func(*args, **kwargs)
        except Exception as error:
            render_message('error', 'Unknown error occured retrying...')
            render_message('error', str(error))
            sleep(5)
            func(*args, **kwargs)
    return decorated_func
