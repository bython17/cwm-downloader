"""
This module is the module that is used by poetry to create
the cli command and the main function is the entry point.
"""
from cwm_downloader import __app_name__
from cwm_downloader.cli import app


def main():
    """ Run the cli """
    app(prog_name=__app_name__)
