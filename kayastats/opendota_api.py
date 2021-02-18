import time
import json
from datetime import datetime

import requests
from tqdm import tqdm

from kayastats import config


def get_pro_matches_list(*, from_date: int = config.CURRENT_PATCH_DATE) -> list:
    """Get a list of pro-matches.

    :param from_date: Unix timestamp of earliest match date in requested list.
    :return: List of matches in json format:
             {
                 "match_id": int,
                 "date": int,
                 "radiant_team": str,
                 "dire_team": str,
                 "radiant_win": bool,
                 "cluster": int,
                 "replay_salt": int,
                 "replay_parsed": bool
             }
    """
    matches_list = []
    last_match_id = None
    url = "https://api.opendota.com/api/proMatches"
    replay_req_url = "https://api.opendota.com/api/replays"

    while True:
        print("Requesting next 100 matches...")
        params = {"less_than_match_id": last_match_id}
        req = requests.get(url, params=params)
        json_response = req.json()

        for match in tqdm(json_response):
            if match["start_time"] > from_date:
                last_match_id = match["match_id"]
                replay_req_params = {"match_id": last_match_id}
                replay_req = requests.get(replay_req_url, params=replay_req_params)
                replay_json_response = replay_req.json()[0]
                matches_list += [{"match_id": match["match_id"],
                                  "date": match["start_time"],
                                  "radiant_team": match["radiant_name"],
                                  "dire_team": match["dire_name"],
                                  "radiant_win": match["radiant_win"],
                                  "cluster": replay_json_response["cluster"],
                                  "replay_salt": replay_json_response["replay_salt"],
                                  "replay_parsed": False}]
                time.sleep(1)  # opendota free tier limit 60 requests per minute
            else:
                print("Date {} reached.".format(from_date))
                print("Total number of matches collected: {}\n".format(len(matches_list)))
                return matches_list
        print("{} matches collected already\n".format(len(matches_list)))
        time.sleep(1)  # opendota free tier limit 60 requests per minute


if __name__ == "__main__":
    pass
