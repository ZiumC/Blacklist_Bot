from parsers import armory_character_parser as armory_parser
import config as conf
from enum import Enum
from models import item_model as im
from models import enchant_model as ench

gs_wrong_count_in_classes = ['Hunter']


class SpecialCharacters:
    WARNING = ':warning:'
    CHECK = ':white_check_mark:'
    CROSS = ':x:'
    WHEEL_CHAIR = ':wheelchair:'
    GEM = ':gem:'
    THINKING = ':thinking:'
    ORANGE_CIRCLE = ':orange_circle:'
    LONG_SPACE = '          '
    LONG_LONG_SPACE = '                    '


class ArmoryFormatter:

    @staticmethod
    def get_messages_of(username):
        character_info, guild_name, guild_link, player_items, player_gs = \
            armory_parser.character_armory(username)

        emoji = SpecialCharacters

        if ((str(80) not in character_info) or
                (not guild_name) or (not guild_link) or
                (not player_items) or (not player_gs)):
            return [emoji.ORANGE_CIRCLE + ' Player **' + username + '** not found in warmane armory ' + emoji.THINKING]

        player_url = conf.ARMORY_URL + username + conf.ARMORY_SERVER

        response = []
        response_details \
            = ('\n' + emoji.WHEEL_CHAIR + ' Summary for: [' + username + '](<' +
               player_url + '>)\n> **Character**: ' + character_info)

        if not guild_link:
            response_details = response_details + '> **Guild**: ' + guild_name + '\n'
        else:
            response_details = response_details + '> **Guild**: [' + guild_name + '](<' + guild_link + '>)\n'

        if 'Hunter' in character_info:
            response_details \
                = (response_details + '> **GearScore**: ' +
                   str(int(player_gs)) + ' ' + emoji.WARNING + ' _(may be inaccurate!)_\n')
        else:
            response_details = response_details + '> **GearScore**: ' + str(int(player_gs)) + '\n'
        response_details = response_details + '> **Gear**:\n'

        items_left = ArmoryFormatter.__get_item_output(0, 6, player_items)
        response_details = response_details + items_left

        response.append(response_details)

        items_right = ArmoryFormatter.__get_item_output(6, 14, player_items)
        items_bottom = ArmoryFormatter.__get_item_output(14, len(player_items), player_items)

        response.append(items_right)
        response.append(items_bottom)

        return response

    @staticmethod
    def __get_item_output(start_index, end_index, player_items):
        emoji = SpecialCharacters
        item_data = ''
        for i in range(start_index, end_index):
            item_data = item_data + '>' + emoji.LONG_SPACE
            item = player_items[i]

            enchant_data = ''
            gem_data = ''
            if isinstance(item, im.Item):
                item_url = conf.ITEM_DATABASE_URL_1 + item.item_id
                item_data = item_data + '__' + item.inventory_type + '__: [' + item.name + '](<' + item_url + '>)\n'
                enchant_data = '>' + emoji.LONG_LONG_SPACE + '__Enchant__: '

                if isinstance(item.enchant, ench.Enchant):
                    enchant_url = conf.ITEM_DATABASE_URL_1 + item.enchant.item_id
                    enchant_data = (enchant_data + '[' + item.enchant.name + '](<' + enchant_url + '>) ' +
                                    emoji.CHECK + '\n')
                elif item.enchant == ' Missing':
                    enchant_data = enchant_data + item.enchant + ' ' + emoji.CROSS + '\n'
                else:
                    enchant_data = ''

                gem_data = '>' + emoji.LONG_LONG_SPACE + '__Gem count__: '
                if item.gems == 'Missing':
                    gem_data = gem_data + item.gems + emoji.CROSS + '\n'
                elif item.gems == 'None':
                    gem_data = ''
                else:
                    gem_data = gem_data + str(item.gems) + ' ' + emoji.GEM + '\n'
            else:
                item_data = item

            item_data = item_data + enchant_data + gem_data
        return item_data
