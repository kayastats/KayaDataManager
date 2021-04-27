from datetime import datetime

from kayastats.opendota_api import get_pro_matches_list
from kayastats.data_manager import save_matches_list
from kayastats import config


if __name__ == "__main__":
    print("\nLoading list of matches...")
    print("\tPatch: {}".format(config.CURRENT_PATCH))
    print("\tFrom date: {}".format(datetime.fromtimestamp(config.CURRENT_PATCH_DATE).strftime("%Y-%m-%d")))
    print("\tTill date (today): {}\n".format(datetime.today().strftime("%Y-%m-%d")))
    matches_list = get_pro_matches_list()
    save_matches_list(matches_list)
    print("\nDone!\nNumber of listed matches: {}\n".format(len(matches_list)))
