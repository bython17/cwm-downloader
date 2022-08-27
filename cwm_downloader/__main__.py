from cwm_downloader.argument_parser import ArgumentParser
from cwm_downloader.utils import initialize_session

with initialize_session() as session:
    ArgumentParser(session)
