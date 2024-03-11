import config as conf
import utils


def get_player_info(player_name):
    url = conf.ARMORY_URL + player_name + conf.ARMORY_SERVER

    html_document = utils.get_html_document(url)
    if is_player_exist(html_document):
        print("Player doesn't exits")
        return
    print("Player exits")
    return


def is_player_exist(html):
    if conf.ARMORY_NOTFOUND_1 in html:
        return True
    if conf.ARMORY_NOTFOUND_2 in html:
        return True
    return False
