from enum import Enum
from typing import Final
from utils import request_util as request
import config as conf
from models import item_model as im
import services.file_service as file


class ItemCategories(Enum):
    ITEM_ID = "ItemID"
    ITEM_NAME = "ItemName"
    ITEM_LEVEL = "itemLevel"
    ITEM_QUALITY = "quality"
    ITEM_INVENTORY_TYPE = "inventoryType"
    ITEM_REQUIRED_LEVEL = "requiredLevel"
    ITEM_HAS_SOCKETS = "hasSockets"


class EnchantedItems(Enum):
    HEAD = 'Head'
    SHOULDER = 'Shoulder'
    CLOAK = 'Cloak'
    CHEST = 'Chest'
    WRIST = 'Wrist'
    HANDS = 'Hands'
    LEGS = 'Legs'
    FEET = 'Feet'
    ONE_HAND = 'One-Hand'
    TWO_HAND = 'Two-Hand'
    MAIN_HAND = 'Main Hand'
    SHIELD = 'Shield'
    RANGED = 'Ranged Right'


item_db = file.read_file_items_db(conf.PATH_TO_ITEM_DB_FILE)
item_categories = [category.lower() for category in item_db[0].split(conf.SEPARATOR)]
enchanted_items = [EnchantedItems.HEAD.value, EnchantedItems.SHOULDER.value, EnchantedItems.CLOAK.value,
                   EnchantedItems.CHEST.value, EnchantedItems.WRIST.value, EnchantedItems.HANDS.value,
                   EnchantedItems.LEGS.value, EnchantedItems.FEET.value, EnchantedItems.ONE_HAND.value,
                   EnchantedItems.TWO_HAND.value, EnchantedItems.MAIN_HAND.value, EnchantedItems.SHIELD.value,
                   EnchantedItems.RANGED.value]


def create_player_item(item_id, enchant_data, gems_data):
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

    player_item = im.Item(item_id, item_name, item_lvl, quality,
                          inventory_type, required_lvl, has_sockets)

    if inventory_type in enchanted_items:
        enchant = __create_enchant(enchant_data)
        setattr(player_item, 'enchant', enchant)
    else:
        setattr(player_item, 'enchant', conf.DEFAULT_ENCHANT_VALUE)

    if has_sockets == str(1):
        gems = __create_gems(gems_data)
        setattr(player_item, 'gems', gems)
    else:
        setattr(player_item, 'gems', conf.DEFAULT_GEMS_VALUE)

    return player_item


def __get_item_detail(raw_item_data, category):
    data_index = item_categories.index(category.lower())
    return raw_item_data[data_index]


def __create_enchant(raw_item_data):
    if not raw_item_data:
        return conf.MISSING_FLAG
    return raw_item_data


def __create_gems(raw_item_data):
    if not raw_item_data:
        return conf.MISSING_FLAG
    return raw_item_data


def __get_raw_item_data(item_id):
    for line in item_db:
        item_id_db = line.split(conf.SEPARATOR)[0]
        if item_id == item_id_db:
            return line