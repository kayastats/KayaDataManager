import requests

from kayastats import config
from kayastats.data_manager import load_matches_list, get_replay_data, \
                                   save_parsed_replay, save_matches_list


def _parse_replay(*, data: bytes) -> bytes:
    parse_req = requests.post(config.REPLAY_PARSER_URL,
                              data=data)
    response_data = parse_req.content
    try:
        if not response_data:
            raise ValueError("Parser returned an empty response")
    except ValueError:
        return b''
    return response_data


def parse(*, matches_list_filename: str) -> None:
    matches_list = load_matches_list(filename=matches_list_filename)
    print("Parsing {} matches...".format(len(matches_list)))
    for match in matches_list:
        if not match["replay_parsed"]:
            replay_data = get_replay_data(match_id=match["match_id"],
                                          cluster=match["cluster"],
                                          replay_salt=match["replay_salt"])
            parsed_data = _parse_replay(data=replay_data)
            if not parsed_data:
                print("Couldn't parse replay with match_id={}".format(match["match_id"]))
                continue
            save_parsed_replay(data=parsed_data, match_id=match["match_id"])
            print("Successfully parsed and saved replay with match_id={}".format(match["match_id"]))
            match["replay_parsed"] = True
            save_matches_list(matches_list, filename=matches_list_filename)
    print("\nAll given matches parsed\n")


if __name__ == "__main__":
    pass
