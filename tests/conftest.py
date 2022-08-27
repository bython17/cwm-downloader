import pytest
from cwm_downloader.utils import initialize_session


def pytest_configure(config):
    plugin = config.pluginmanager.getplugin('mypy')
    plugin.mypy_argv.append('--check-untyped-defs')


@pytest.fixture
def request_session():
    session = initialize_session()
    return session
