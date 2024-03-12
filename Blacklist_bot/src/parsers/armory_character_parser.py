import config as conf
from utils import request
from parsers import item_parser
import re
from typing import Final

DIV_CLASS_REGEX: Final[str] = '<div class=\"level-race-class\">.*\\s*.*\\s*.*>$'
DIV_LEFT_REGEX: Final[str] = '<div class=\"item-left\">((.|\n)*)<div class=\"item-right\">'
DIV_RIGHT_REGEX: Final[str] = '<div class=\"item-right\">((.|\n)*)<div class=\"item-bottom\">'
DIV_BOTTOM_REGEX: Final[str] = '<div class=\"item-bottom\">((.|\n)*)<div class=\"model\">'
ITEM_DATA_REGEX: Final[str] = '=\"item={1}.*\"'


def get_player_items(character_name):
    url = conf.ARMORY_URL + character_name + conf.ARMORY_SERVER
    html_document = request.get_html_document(url)

    if __player_exist(html_document):
        return "Player doesn't exits, given input: " + character_name

    items_data = __get_items(html_document, DIV_LEFT_REGEX, ITEM_DATA_REGEX, True)
    items_data.extend(__get_items(html_document, DIV_RIGHT_REGEX, ITEM_DATA_REGEX, False))
    items_data.extend(__get_items(html_document, DIV_BOTTOM_REGEX, ITEM_DATA_REGEX, False))

    item_objects = []
    for item in items_data:
        item_extract = item.split('&')
        item_id = item_extract[0]
        item_enchant_or_gem = ''

        if len(item_extract) > 1:
            item_enchant_or_gem = item_extract[1]

        item_objects.append(item_parser.create_item(item_id, item_enchant_or_gem))

    return item_objects


def __get_items(html_document, pattern_1, pattern_2, is_left):
    try:
        div_element = re.search(pattern_1, html_document).group(1)
        div_items = re.findall(pattern_2, div_element)

        items = []
        for item in div_items:
            item_data = item.replace('\"', '')
            item_data = item_data.replace('=item=', '')
            items.append(item_data)

        # Need to remove Shirt and Tabard item slots
        if is_left and len(items) > 6:
            wrist_item = items.pop()
            del items[5:]
            items.append(wrist_item)

        return items
    except AttributeError:
        return "Unable to find items. Regex: r1=" + pattern_1 + ", r2=" + pattern_2


def __player_exist(html):
    if conf.ARMORY_NOTFOUND_1 in html:
        return True
    if conf.ARMORY_NOTFOUND_2 in html:
        return True
    return False
