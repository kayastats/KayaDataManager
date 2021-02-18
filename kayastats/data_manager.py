import json
from datetime import datetime

from kayastats import config


def save_matches_list(matches_list: list, *, pro_matches: bool):
    current_date = datetime.today().strftime('%Y-%m-%d')
    filename = "matches_list_" + current_date + ".json"
    if pro_matches:
        filename = "pro_" + filename
    with open(config.MATCHES_LIST_PATH / filename, 'w', encoding='utf-8') as f:
        json.dump(matches_list, f, ensure_ascii=False, indent=4)


# TODO: refactor load_matches_list to work without exact filename provided
def load_matches_list(*, filename: str) -> list:
    with open(config.MATCHES_LIST_PATH / filename) as json_file:
        matches_list = json.load(json_file)
    return matches_list

if __name__ == "__main__":
    pass
