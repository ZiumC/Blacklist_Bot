from parsers import armory_character_parser as armory_parser
import config as conf
from enum import Enum
from models import item_model as im
from models import enchant_model as ench

gs_wrong_count_in_classes = ['Hunter']


class SpecialCharacters(Enum):
    WARNING = ':warning:'
    CHECK = ':white_check_mark:'
    CROSS = ':x:'
    WHEEL_CHAIR = ':wheelchair:'
    GEM = ':gem:'
    LONG_SPACE = '          '
    LONG_LONG_SPACE = '                    '


class ArmoryFormatter:

    def get_messages_of(self, username):
        character_info, guild_name, guild_link, player_items, player_gs = \
            armory_parser.character_armory(username)
        player_url = conf.ARMORY_URL + username + conf.ARMORY_SERVER

        response_details \
            = ('\n' + SpecialCharacters.WHEEL_CHAIR.value + ' Summary for: [' + username + '](<' +
               player_url + '>)\n> **Character**: ' + character_info)

        if not guild_link:
            response_details = response_details + '> **Guild**: ' + guild_name + '\n'
        else:
            response_details = response_details + '> **Guild**: [' + guild_name + '](<' + guild_link + '>)\n'

        if 'Hunter' in character_info:
            response_details \
                = (response_details + '> **GearScore**: ' +
                   str(int(player_gs)) + ' ' + SpecialCharacters.WARNING.value + ' _(may be inaccurate!)_\n')
        else:
            response_details = response_details + '> **GearScore**: ' + str(int(player_gs)) + '\n'
        response_details = response_details + '> **Gear**:\n'

        item_data = ''
        for i in range(0, 6):
            item_data = item_data + '>' + SpecialCharacters.LONG_SPACE.value
            item = player_items[i]

            enchant_data = ''
            gem_data = ''
            if isinstance(item, im.Item):
                item_url = conf.ITEM_DATABASE_URL_1 + item.item_id
                item_data = item_data + '__' + item.item_type + '__: [' + item.name + '](<' + item_url + '>)\n'
                enchant_data = '>' + SpecialCharacters.LONG_LONG_SPACE.value + '__Enchant__: '

                if isinstance(item.enchant, ench.Enchant):
                    enchant_url = conf.ITEM_DATABASE_URL_1 + item.enchant.item_id
                    enchant_data = (enchant_data + '[' + item.enchant.name + '](<' + enchant_url + '>) ' +
                                    SpecialCharacters.CHECK.value + '\n')
                elif item.enchant == ' Missing':
                    enchant_data = enchant_data + item.enchant + ' ' + SpecialCharacters.CROSS.value + '\n'
                else:
                    enchant_data = ''

                gem_data = '>' + SpecialCharacters.LONG_LONG_SPACE.value + '__Gem count__: '
                if item.gems == 'Missing':
                    gem_data = gem_data + item.gems + SpecialCharacters.CROSS.value + '\n'
                elif item.gems == 'None':
                    gem_data = ''
                else:
                    gem_data = gem_data + str(item.gems) + ' ' + SpecialCharacters.GEM.value + '\n'
            else:
                item_data = item

            item_data = item_data + enchant_data + gem_data
        response_details = response_details + item_data

        return response_details
    
