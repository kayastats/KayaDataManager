import pathlib
from datetime import datetime

import parser_manager


PACKAGE_ROOT = pathlib.Path(parser_manager.__file__).resolve().parent

CURRENT_PATCH = '7.28'
CURRENT_PATCH_DATE = datetime.strptime('2020-12-18', "%Y-%m-%d").timestamp()

COLLECTED_DATA_PATH = PACKAGE_ROOT / 'collected_data'
