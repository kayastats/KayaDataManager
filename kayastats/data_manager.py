import sys
import json
from datetime import datetime

import requests
import bz2

from kayastats import config


def save_matches_list(matches_list: list, *, filename: str = "", pro_matches: bool = False) -> None:
    if filename == "":
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


def get_replay_data(*, match_id: int, cluster: int, replay_salt: int) -> bytes:
    print("\nLoading replay with match_id={}... (this may take some time)".format(match_id))
    replay_url = "http://replay{0}.valve.net/570/{1}_{2}.dem.bz2".format(cluster,
                                                                         match_id,
                                                                         replay_salt)
    replay_req = requests.get(replay_url, allow_redirects=True)
    try:
        if replay_req.status_code != 200:
            raise ConnectionError("Can't load replay with match_id={}".format(match_id))
    except ConnectionError:
        return b''
    replay_data = bz2.decompress(replay_req.content)
    replay_size = sys.getsizeof(replay_data) / (1024*1024)  # size in megabytes
    print("Finished loading replay with match_id={}, size: {:.1f} MB".format(match_id, replay_size))
    return replay_data


def save_parsed_replay(*, data: bytes, match_id: int) -> None:
    filename = str(match_id) + ".jsonl"
    with open(config.PARSED_REPLAYS_PATH / filename, 'wb') as f:
        f.write(data)


if __name__ == "__main__":
    pass
