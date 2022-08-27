from src.argument_parser import ArgumentParser
from src.utils import initialize_session

with initialize_session() as session:
    ArgumentParser(session)
