import requests
import time
import json
from datetime import datetime

from parser_manager import config


def get_matches_list(*, from_date: int = config.CURRENT_PATCH_DATE) -> list:
    matches_list = []
    last_match_id = None
    url = "https://api.opendota.com/api/proMatches"

    while True:
        params = {"less_than_match_id": last_match_id}
        req = requests.get(url, params=params)
        json_response = req.json()

        for match in json_response:
            if match["start_time"] > from_date:
                matches_list += [{"match_id": match["match_id"],
                                  "date": match["start_time"],
                                  "radiant_team": match["radiant_name"],
                                  "dire_team": match["dire_name"],
                                  "radiant_win": match["radiant_win"]}]
                last_match_id = match["match_id"]
            else:
                print("Date {} reached.".format(from_date))
                print("Total number of matches collected: {}\n".format(len(matches_list)))
                return matches_list
        print("{} matches collected already, requesting new...".format(len(matches_list)))
        time.sleep(1)  # opendota free tier limit 60 requests per minute


if __name__ == "__main__":
    matches_list = get_matches_list(from_date=1612904400)
    current_date = datetime.today().strftime('%Y-%m-%d')
    filename = "matches_list_" + current_date + ".json"
    with open(config.COLLECTED_DATA_PATH / filename, 'w', encoding='utf-8') as f:
        json.dump(matches_list, f, ensure_ascii=False, indent=4)
