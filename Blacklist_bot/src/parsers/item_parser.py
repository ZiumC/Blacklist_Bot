from enum import Enum
from typing import Final
from utils import request_util as request
import config as conf
from models import item_model as im
from models import enchant_model as ench
import services.file_service as file


class ItemAdditionType(Enum):
    GEM = "Gem"
    ENCHANT = "Enchant"


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


item_db = file.read_db_file(conf.PATH_TO_ITEM_DB_FILE)
enchant_id_item_id_db = file.read_db_file(conf.PATH_TO_ENCHANT_TRANSLATION_FILE)
item_categories = [category.lower() for category in item_db[0].split(conf.SEPARATOR)]
enchanted_items = [EnchantedItems.HEAD.value, EnchantedItems.SHOULDER.value, EnchantedItems.CLOAK.value,
                   EnchantedItems.CHEST.value, EnchantedItems.WRIST.value, EnchantedItems.HANDS.value,
                   EnchantedItems.LEGS.value, EnchantedItems.FEET.value, EnchantedItems.ONE_HAND.value,
                   EnchantedItems.TWO_HAND.value, EnchantedItems.MAIN_HAND.value, EnchantedItems.SHIELD.value,
                   EnchantedItems.RANGED.value]


def create_player_item(item_id, enchant_data, gems_data):
    raw_item_data = __get_raw_item_data(item_id)
    if raw_item_data is None:
        return conf.DEFAULT_NOT_EXIST_VALUE

    raw_item_array = raw_item_data.split(conf.SEPARATOR)

    item_name = __get_item_property(raw_item_array, ItemCategories.ITEM_NAME.value)
    item_lvl = __get_item_property(raw_item_array, ItemCategories.ITEM_LEVEL.value)
    quality = __get_item_property(raw_item_array, ItemCategories.ITEM_QUALITY.value)
    inventory_type = __get_item_property(raw_item_array, ItemCategories.ITEM_INVENTORY_TYPE.value)
    required_lvl = __get_item_property(raw_item_array, ItemCategories.ITEM_REQUIRED_LEVEL.value)
    has_sockets = __get_item_property(raw_item_array, ItemCategories.ITEM_HAS_SOCKETS.value)

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


def __get_item_property(raw_item_array, category):
    data_index = item_categories.index(category.lower())
    return raw_item_array[data_index]


def __create_enchant(enchant_data_line):
    if not enchant_data_line:
        return conf.MISSING_FLAG

    enchant_id = enchant_data_line.replace("ench=", '')
    item_id = __translate_addition_to_item_id(enchant_id, ItemAdditionType.ENCHANT.value)

    if item_id == -1:
        return conf.DEFAULT_NOT_EXIST_VALUE + " but exist on item"

    raw_enchant_array = __get_raw_item_data(item_id).split(conf.SEPARATOR)
    item_name = __get_item_property(raw_enchant_array, ItemCategories.ITEM_NAME.value)
    item_lvl = __get_item_property(raw_enchant_array, ItemCategories.ITEM_LEVEL.value)
    quality = __get_item_property(raw_enchant_array, ItemCategories.ITEM_QUALITY.value)

    return ench.Enchant(item_id, item_name, item_lvl, quality)


# At the moment I don't have db file: gemID -> itemID
# This is the reason why it is like this
def __create_gems(gems_data_line):
    if not gems_data_line:
        return conf.MISSING_FLAG
    gems_array = gems_data_line.replace('gems=', '').split(':')

    gem_counter = 0
    for gem in gems_array:
        if gem != str('0'):
            gem_counter = +1

    return gem_counter


def __translate_addition_to_item_id(enchant_id, item_addition_type):
    if item_addition_type == ItemAdditionType.ENCHANT.value:
        item_raw_data = __get_raw_item_data(enchant_id, db=enchant_id_item_id_db, search_by_index=1, separator='\t')
        if not item_raw_data:
            return -1
        return item_raw_data.split('\t')[0]
    return "Addition type is not supported"


def __get_raw_item_data(item_id, db=item_db, search_by_index=0, separator=conf.SEPARATOR):
    for line in db:
        item_id_db = line.split(separator)[search_by_index]
        if item_id in item_id_db:
            return line
