from json import loads


def get_element_selectors(json_filepath: str = './scraper') -> dict[str, list[str]]:
    with open(f"{json_filepath}/element_selectors.json", 'r') as file:
        return loads(file.read())
