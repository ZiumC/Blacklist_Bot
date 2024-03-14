from parsers import armory_character_parser as armory_parser
import config as conf
from enum import Enum



class ArmoryFormatter:

    @staticmethod
    def get_messages_of(username):
        character_info, guild_name, guild_link, player_items, player_gs = \
            armory_parser.character_armory(username)
        print(character_info)
        print(guild_name)
        print(guild_link)
        print(player_items)
        print(player_gs)
        print("items")
        for i in player_items:
            print(i.name)
            print(i.enchant)
            print(i.gems)
            print("-----")

        return
