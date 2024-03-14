import config as conf
from utils import request_util as request
from parsers import item_parser
from models import enchant_model as ench
from models import item_model as im
from services import gearscore_service as gs
import re
from typing import Final

DIV_CHARACTER_REGEX: Final[str] = 'L.+\\d+.+([\r\n\\s]+)</'
SPAN_GUILD_REGEX: Final[str] = '<span class=\"guild-name\">.+</span>'
LINK_REGEX: Final[str] = 'href=\".+\"'
GUILD_REGEX: Final[str] = '<a.+>.+</a'
DIV_LEFT_REGEX: Final[str] = '<div class=\"item-left\">((.|\n)*)<div class=\"item-right\">'
DIV_RIGHT_REGEX: Final[str] = '<div class=\"item-right\">((.|\n)*)<div class=\"item-bottom\">'
DIV_BOTTOM_REGEX: Final[str] = '<div class=\"item-bottom\">((.|\n)*)<div class=\"model\">'
ITEM_DATA_REGEX: Final[str] = '=\"item={1}.*\"'
ENCHANT_REGEX: Final[str] = 'ench=\\d*'
GEMS_REGEX: Final[str] = 'gems=.*'


def character_armory(character_name):
    try:
        url = conf.ARMORY_URL + character_name + conf.ARMORY_SERVER
        html_document = request.get_html_document(url)

        if __player_exist(html_document):
            return "Player doesn't exits, given input: " + character_name

        player_items, player_gs = __get_player_items(html_document)
        character_info, guild_name, guild_link = __get_character_info(html_document)
        return character_info, guild_name, guild_link, player_items, player_gs

    except Exception as e:
        print(e)
        raise e


def __get_character_info(html_document):
    character_data = __extract_data(html_document, DIV_CHARACTER_REGEX)
    character_data = character_data.replace('</', '')
    html_guild_data = __extract_data(html_document, SPAN_GUILD_REGEX)
    guild_link = (
            conf.BASE_ARMORY_URL + __extract_data(html_guild_data, LINK_REGEX).replace('href="', '').replace('"', ''))
    guild_name = __extract_data(html_guild_data, GUILD_REGEX).split('">')[1].replace('</a', '')
    return character_data, guild_name, guild_link


def __extract_data(html_elem, pattern_1):
    p = re.compile(pattern_1)
    return p.search(html_elem).group(0)


def __get_player_items(html_document):
    items_data = __extract_item_data(html_document, DIV_LEFT_REGEX, ITEM_DATA_REGEX, True)
    items_data.extend(__extract_item_data(html_document, DIV_RIGHT_REGEX, ITEM_DATA_REGEX, False))
    items_data.extend(__extract_item_data(html_document, DIV_BOTTOM_REGEX, ITEM_DATA_REGEX, False))

    gs_list = []
    item_objects = []
    for item in items_data:
        item_id = item.split('&')[0]
        item_enchant = __get_additions_item_(item, ENCHANT_REGEX)
        item_gems = __get_additions_item_(item, GEMS_REGEX)

        player_item = item_parser.create_player_item(item_id, item_enchant, item_gems)

        if not isinstance(player_item, im.Item):
            return player_item

        item_gs = gs.get_item_gear_score(player_item)
        gs_list.append(item_gs)
        item_objects.append(player_item)
        print("-------------")
        print(player_item.item_id)
        print(player_item.name)
        print(player_item.item_lvl)
        print(player_item.quality)
        print(player_item.inventory_type)
        print(player_item.required_lvl)
        print(player_item.has_sockets)
        if not isinstance(player_item.enchant, ench.Enchant):
            print(player_item.enchant)
        else:
            print("~~enchant:")
            print(player_item.enchant.item_id)
            print(player_item.enchant.name)
            print(player_item.enchant.item_lvl)
            print(player_item.enchant.quality)
            print("~~~")
        print(player_item.gems)
        print("-------------")
        print("GS:" + str(item_gs))
    return item_objects, sum(gs_list)


def __player_exist(html):
    if conf.ARMORY_NOTFOUND_1 in html:
        return True
    if conf.ARMORY_NOTFOUND_2 in html:
        return True
    return False


def __extract_item_data(html_document, pattern_1, pattern_2, is_left):
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


def __get_additions_item_(item_data, pattern_1):
    try:
        pattern = re.compile(pattern_1)
        all_elements = pattern.findall(item_data)
        if len(all_elements) == 1:
            return all_elements[0]
        return
    except AttributeError:
        return "Unable to find item. Regex: r1=" + pattern_1
