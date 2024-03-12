from enum import Enum
from typing import Final
from utils import request_util as request
import config as conf
from models import item_model as im
import services.file_service as file

item_db = file.read_file_items_db(conf.PATH_TO_ITEM_DB_FILE)
item_categories = [category.lower() for category in item_db[0].split(conf.SEPARATOR)]


class ItemCategories(Enum):
    ITEM_ID = "ItemID"
    ITEM_NAME = "ItemName"
    ITEM_LEVEL = "itemLevel"
    ITEM_QUALITY = "quality"
    ITEM_INVENTORY_TYPE = "inventoryType"
    ITEM_REQUIRED_LEVEL = "requiredLevel"
    ITEM_HAS_SOCKETS = "hasSockets"


def create_player_item(item_id, item_enchant_or_gem):
    raw_item_data = __get_raw_item_data(item_id)
    if raw_item_data is None:
        return "Unable to find item data by id: " + item_id

    raw_item_array = raw_item_data.split(conf.SEPARATOR)

    item_name = __get_item_detail(raw_item_array, ItemCategories.ITEM_NAME.value)
    item_lvl = __get_item_detail(raw_item_array, ItemCategories.ITEM_LEVEL.value)
    quality = __get_item_detail(raw_item_array, ItemCategories.ITEM_QUALITY.value)
    inventory_type = __get_item_detail(raw_item_array, ItemCategories.ITEM_INVENTORY_TYPE.value)
    required_lvl = __get_item_detail(raw_item_array, ItemCategories.ITEM_REQUIRED_LEVEL.value)
    has_sockets = __get_item_detail(raw_item_array, ItemCategories.ITEM_HAS_SOCKETS.value)

    return im.Item(item_id, item_name, item_lvl, quality, inventory_type, required_lvl, has_sockets)


def __get_item_detail(raw_item_data, category):
    data_index = item_categories.index(category.lower())
    return raw_item_data[data_index]


def __create_item(raw_item_data):
    return


def __get_raw_item_data(item_id):
    for line in item_db:
        item_id_db = line.split(conf.SEPARATOR)[0]
        if item_id == item_id_db:
            return line
