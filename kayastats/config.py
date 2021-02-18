import pathlib
from datetime import datetime

import kayastats


PACKAGE_ROOT = pathlib.Path(kayastats.__file__).resolve().parent

CURRENT_PATCH = '7.28'
CURRENT_PATCH_DATE = datetime.strptime('2020-12-18', "%Y-%m-%d").timestamp()

MATCHES_LIST_PATH = PACKAGE_ROOT / 'collected_data'
