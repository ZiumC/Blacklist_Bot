from parsers import armory_character_parser as armory_parser
import config as conf
from enum import Enum

gs_wrong_count_in_classes = ['Hunter']


class SpecialCharacters(Enum):
    WARNING = ':warning:'
    CHECK = ':white_check_mark:'
    CROSS = ':x:'
    WHEEL_CHAIR = ':wheelchair:'


class ArmoryFormatter:

    @staticmethod
    def get_messages_of(username):
        character_info, guild_name, guild_link, player_items, player_gs = \
            armory_parser.character_armory(username)
        player_url = conf.ARMORY_URL + username + conf.ARMORY_SERVER

        response_details = (
                '\n' + SpecialCharacters.WHEEL_CHAIR.value + ' Summary for: [' + username + '](<' +
                player_url + '>)\n> **Character**: ' + character_info
        )

        if not guild_link:
            response_details = response_details + '> **Guild**: ' + guild_name + '\n'
        else:
            response_details = response_details + '> **Guild**: [' + guild_name + '](<' + guild_link + '>)\n'

        if 'Hunter' in character_info:
            response_details = (response_details + '> **GearScore**: ' + str(int(player_gs)) + ' ' +
                                SpecialCharacters.WARNING.value + ' (may be inaccurate!)\n')
        else:
            response_details = response_details + '> **GearScore**: ' + str(int(player_gs)) + '\n'

        return response_details
