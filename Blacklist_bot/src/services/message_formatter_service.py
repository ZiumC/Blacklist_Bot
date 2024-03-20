from parsers import armory_character_parser as armory_parser
import config as conf
from models import item_model as im
from models import enchant_model as ench
from message_handler import Handler as messHandler

gs_wrong_count_in_classes = ['Hunter']


class SpecialCharacters:
    WARNING = ':warning:'
    CHECK = ':white_check_mark:'
    CROSS = ':x:'
    WHEEL_CHAIR = ':wheelchair:'
    GEM = ':gem:'
    THINKING = ':thinking:'
    ORANGE_CIRCLE = ':orange_circle:'
    GREEN_CIRCLE = ':green_circle:'
    STOP_SIGN = ':octagonal_sign:'
    ANGRY_FACE = ':face_with_symbols_over_mouth:'
    INFO_SIGN = ':information_source:'
    DIAMOND_SIGN = ':large_blue_diamond:'
    ARROW_SIGN = ':arrow_right:'
    CRAZY_FACE = ':woozy_face:'
    BROKEN_HEART = ':broken_heart:'
    HEART = ':heart:'
    CRY_FACE = ':cry:'
    HOUR_GLASS = ':hourglass_flowing_sand:'
    LONG_SPACE = '          '
    LONG_LONG_SPACE = '                    '


emoji = SpecialCharacters


class AdminCommandFormatter:
    @staticmethod
    def format_help(commands_list):
        response = emoji.GREEN_CIRCLE + ' Available commands in chat **#' + conf.MODERATION_CHANNEL_BL + '** are:\n'
        response = response + '1) **' + commands_list[0] + '**\n'
        response = response + '2) **' + commands_list[1] + '** [username] -[description]\n'
        response = response + '3) **' + commands_list[2] + '** [username] -[description]\n'
        response = response + '4) **' + commands_list[3] + '** [username]\n'
        response = response + '5) **' + commands_list[4] + '**\n'
        response = response + '6) **' + commands_list[5] + '** [type] (type can be: CRITICAL, ERROR, WARNING)\n'
        response = response + '7) **' + commands_list[6] + '** (viable for creator)\n'
        response = response + emoji.DIAMOND_SIGN + (' If you want write only announce message, just type'
                                                    ' character **$** before your message and bot will ignore it.')
        return response

    @staticmethod
    def format_last_added(username, added_by, date_added, reason):
        response = emoji.ORANGE_CIRCLE + ' Last added player to blacklist is **' + username + '**\n\n'

        response = (response + emoji.INFO_SIGN + '  Player has been added by **' + added_by + '** at **' +
                    date_added + '**\n')
        response_messages = [response]
        response_messages.extend(PublicCommandFormatter.format_bl_reason(reason))
        return response_messages

    @staticmethod
    def format_forgotten_sign_error():
        return emoji.CROSS + ' Did you forget about mark: \' - \'? ' + emoji.THINKING

    @staticmethod
    def format_unknown_command_error(command, commands_list):
        return (emoji.CROSS + 'Unable to resolve command **' + command + '**.\n\n'
                + AdminCommandFormatter.format_help(commands_list))

    @staticmethod
    def format_player_exist_error(username, modify_command):
        return (emoji.WARNING + ' Player **' + username +
                '** already exist in blacklist. Instead of adding new one maybe consider to use command **' +
                modify_command + '**? ' + emoji.CRAZY_FACE)

    @staticmethod
    def format_add_success(username):
        return emoji.GREEN_CIRCLE + ' Player **' + username + '** has been added to blacklist! ' + emoji.HEART

    @staticmethod
    def format_notfound_error(username):
        return emoji.CROSS + ' Player **' + username + '** not found at blacklist ' + emoji.CRY_FACE

    @staticmethod
    def format_update_success(username):
        return emoji.GREEN_CIRCLE + ' Player **' + username + '** has been updated ' + emoji.HEART

    @staticmethod
    def format_command_error(username, command):
        response = (emoji.CROSS + ' Unable to perform command **' + command + '** for player **' + username + '** data '
                    + emoji.BROKEN_HEART + '\n')
        response = response + 'Contact ASAP with Toxic Rafał'
        return response

    @staticmethod
    def format_delete_success(username):
        return emoji.GREEN_CIRCLE + ' Player **' + username + '** has been deleted from blacklist!'

    @staticmethod
    def format_players_notfound_error():
        return emoji.WARNING + ' Blacklist is empty! ' + emoji.WARNING

    @staticmethod
    def format_log_output(log_err_type, log_lines):
        response_messages = []
        if len(log_lines) > 0:
            response = '```'
            for line in log_lines:
                if len(response) > (conf.MAX_DISCORD_MESSAGE_LENGTH - 150):
                    response_messages.append(response + '```')
                    response = '```'
                else:
                    response = response + line
            response = response + '```'
            response_messages.append(response)
            return response_messages

        return ['Log doesn\'t contains any line with **' + log_err_type + '**']


class PublicCommandFormatter:
    @staticmethod
    def format_bl_warning(username, added_by, date_added):
        response = emoji.STOP_SIGN + ' Player **' + username + '** exist on black list! ' + emoji.ANGRY_FACE + '\n\n'

        response = (response + emoji.INFO_SIGN + ' Player **' + username + '** has been added to black list by **' +
                    added_by + ' ** at **' + date_added + '**.')

        return response

    @staticmethod
    def format_bl_reason(reason):
        response = []

        if len(reason) > conf.MAX_DISCORD_MESSAGE_LENGTH:
            reason_chunks = messHandler.divide_message(reason, conf.MAX_DISCORD_MESSAGE_LENGTH)
            for reason_line in reason_chunks:
                response.append(reason_line)
        else:
            response.append(emoji.ARROW_SIGN + ' Reason: ' + reason)

        return response

    @staticmethod
    def format_bl_notfound():
        response = [emoji.CHECK + ' Player **notfound** on blacklist',
                    emoji.HOUR_GLASS + ' Generating armory report...']
        return response

    @staticmethod
    def format_help(command_list):
        response = emoji.GREEN_CIRCLE + ' Available commands in chat **#' + conf.PUBLIC_CHANNEL_BL + '** are:\n'
        response = response + '1) **' + command_list[0] + '**\n'
        response = response + '2) **' + command_list[1] + '**  [username]\n'
        return response

    @staticmethod
    def format_error(command, commands_list):
        return (emoji.CROSS + ' unable to resolve command **' + command + '**\n\n'
                + PublicCommandFormatter.format_help(commands_list))


class ArmoryFormatter:

    @staticmethod
    def get_messages_of(username):
        character_info, guild_name, guild_link, player_items, player_gs = \
            armory_parser.character_armory(username)

        if ((str(80) not in character_info) or
                ((not guild_name) and (not guild_link) and
                 (not player_items) and (not player_gs))):
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

        warning_has_added = False
        for character_class in gs_wrong_count_in_classes:
            if character_class in character_info:
                response_details \
                    = (response_details + '> **GearScore**: ' +
                       str(int(player_gs)) + ' ' + emoji.WARNING + ' _(may be inaccurate!)_\n')
                warning_has_added = True
                break

        item_has_0_gs = False
        for item in player_items:
            if str(item.item_gs) == '0':
                item_has_0_gs = True

        if not warning_has_added:
            if item_has_0_gs:
                response_details \
                    = (response_details + '> **GearScore**: ' +
                       str(int(player_gs)) + ' ' + emoji.WARNING + ' _(one or many items has 0 GS)_\n')
            else:
                response_details = response_details + '> **GearScore**: ' + str(int(player_gs)) + '\n'
        response_details = response_details + '> **Gear**:\n'

        items_0 = ArmoryFormatter.__get_item_output(0, 4, player_items)
        response_details = response_details + items_0

        response.append(response_details)

        items_1 = ArmoryFormatter.__get_item_output(4, 8, player_items)
        response.append(items_1)

        items_2 = ArmoryFormatter.__get_item_output(8, 12, player_items)
        response.append(items_2)

        items_3 = ArmoryFormatter.__get_item_output(12, 14, player_items)
        response.append(items_3)

        items_4 = ArmoryFormatter.__get_item_output(14, len(player_items), player_items)
        response.append(items_4)

        return response

    @staticmethod
    def __get_item_output(start_index, end_index, player_items):
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
                elif 'Exist on item' in item.enchant:
                    enchant_data = enchant_data + item.enchant + ' ' + emoji.CHECK + '\n'
                    enchant_data = enchant_data + '>' + emoji.LONG_LONG_SPACE + '_(Translation enchantID -> itemID notfound)_\n'
                else:
                    enchant_data = ''

                gem_data = '>' + emoji.LONG_LONG_SPACE + '__Gem count__: '
                if item.gems == 'Missing':
                    gem_data = gem_data + item.gems + emoji.CROSS + '\n'
                elif item.gems == 'None':
                    gem_data = ''
                else:
                    gem_data = gem_data + str(item.gems) + ' ' + emoji.GEM + '\n'

                missing_gs = ''
                if str(0) == str(item.item_gs):
                    missing_gs = ('>' + emoji.LONG_LONG_SPACE + '__Item GS__: '
                                  + str(item.item_gs) + ' ' + emoji.WARNING + '\n')
                gem_data = gem_data + missing_gs
            else:
                item_data = item

            item_data = item_data + enchant_data + gem_data
        return item_data
