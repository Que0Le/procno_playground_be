import os

from app.core.config import settings
from app.utilities import utils, strings


def get_valid_random_record_filename():
    tries = 10
    while tries > 0:
        tries = tries - 1
        filename = strings.random_alphanumeric(length=32)
        if not os.path.isfile(f"{settings.DATA_PATH}/records/" + filename):
            return filename
    return ""