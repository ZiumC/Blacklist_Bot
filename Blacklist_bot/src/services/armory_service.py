import config as conf
import utils
from typing import Final


DIV_CLASS_REGEX: Final[str] = '<div class="level-race-class">.*\\s*.*\\s*.*>$'
DIV_LEFT_REGEX: Final[str] = '<div class="item-left">((.|\n)*)<div class="item-right">'
DIV_RIGHT_REGEX: Final[str] = '<div class="item-right">((.|\n)*)<div class="item-bottom">'
DIV_BOTTOM_REGEX: Final[str] = '<div class="item-bottom">((.|\n)*)<div class="model">'
ITEM_DATA_REGEX: Final[str] = '="item={1}.*"'


def get_player_info(player_name):
    url = conf.ARMORY_URL + player_name + conf.ARMORY_SERVER

    html_document = utils.get_html_document(url)
    if player_exist(html_document):
        print("Player doesn't exits")
        return

    print("Player exits")
    print(html_document)
    return


def player_exist(html):
    if conf.ARMORY_NOTFOUND_1 in html:
        return True
    if conf.ARMORY_NOTFOUND_2 in html:
        return True
    return False


def get_item_id():
    return

def get_item_enchant_id():
    return


