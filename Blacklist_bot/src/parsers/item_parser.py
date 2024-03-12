from typing import Final
from utils import request
import config as conf
import services.file_service as file

DIV_CLASS_REGEX: Final[str] = ''


def create_player_item(item_id, item_enchant_or_gem):
    item_data = file.et_raw_item_data(conf.PATH_TO_ITEM_DB_FILE, item_id)
    return


def __get_item_details(item_data):
    return
