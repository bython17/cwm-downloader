#! /usr/bin/env python
from functools import partial
from cwm_downloader.cli import app as _app
from sys import argv


app = partial(_app, prog_name='cwm-downloader')


def main():
    if len(argv) == 1:
        app(['--help'])
    if '--edit-credentials' in argv:
        app(['--edit-credentials', 'https://codewithmosh.com'])
    else:
        app()
