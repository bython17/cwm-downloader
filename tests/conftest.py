def pytest_configure(config):
    plugin = config.pluginmanager.getplugin('mypy')
    plugin.mypy_argv.append('--check-untyped-defs')
