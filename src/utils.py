from json import loads


def get_element_selectors(json_filepath: str = './') -> dict[str, list[str]]:
    with open(json_filepath, 'r') as file:
        return loads(file.read())
