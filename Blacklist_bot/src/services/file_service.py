import os
import logging
from datetime import date
from datetime import datetime
import config as conf
from safe_str import SafeStr as sStr


def add_user_to_bl(who_added, username_to_bl, description):
    file = open(conf.PATH_TO_BLOCKED_USERS_FILE, mode="a")
    if os.path.exists(conf.PATH_TO_BLOCKED_USERS_FILE):
        file.write(prepare_line_to_write(who_added, username_to_bl, description))
        file.close()
        return True
    else:
        logging.critical(
            "Path is invalid or doesn't exist. Path should also contain destination file: path="
            + conf.PATH_TO_BLOCKED_USERS_FILE + ",method=" + add_user_to_bl.__name__
        )
        return False


def remove_user_from_bl(username_to_remove):
    is_removed = False
    if os.path.exists(conf.PATH_TO_BLOCKED_USERS_FILE):
        with open(conf.PATH_TO_BLOCKED_USERS_FILE, "r") as file:
            all_lines = file.readlines()
        with open(conf.PATH_TO_BLOCKED_USERS_FILE, "w") as file:
            for line in all_lines:
                username_from_file = line.split(",")[0]
                if username_from_file == username_to_remove:
                    is_removed = True
                    pass
                else:
                    file.write(line)
        logging.info(
            "Removing player: player=" + username_to_remove
            + ",status=" + str(is_removed) + ",method=" + remove_user_from_bl.__name__
        )
        return is_removed
    else:
        logging.critical(
            "Path is invalid or doesn't exist. Path should also contain destination file: path="
            + conf.PATH_TO_BLOCKED_USERS_FILE + ",method=" + remove_user_from_bl.__name__
        )
        return False


def get_user_data(username_to_check):
    if os.path.exists(conf.PATH_TO_BLOCKED_USERS_FILE):
        with open(conf.PATH_TO_BLOCKED_USERS_FILE, "r") as file:
            all_lines = file.readlines()
        for line in all_lines:
            username_from_file = line.split(",")[0]
            if username_from_file == username_to_check:
                return line
        logging.warning(
            "Empty line has been returned: player="
            + username_to_check + ",method=" + get_user_data.__name__
        )
        return ""
    else:
        logging.critical(
            "Path is invalid or doesn't exist. Path should also contain destination file: path="
            + conf.PATH_TO_BLOCKED_USERS_FILE + ",method=" + get_user_data.__name__
        )
        return ""


def update_user_data(who_updated, username, description):
    is_updated = False
    if os.path.exists(conf.PATH_TO_BLOCKED_USERS_FILE):
        with open(conf.PATH_TO_BLOCKED_USERS_FILE, "r") as file:
            all_lines = file.readlines()
        with open(conf.PATH_TO_BLOCKED_USERS_FILE, "w") as file:
            for line in all_lines:
                username_from_file = line.split(",")[0]
                if username_from_file == username:
                    file.write(prepare_line_to_write(who_updated, username, description))
                    is_updated = True
                else:
                    file.write(line)
            logging.info(
                "Updating player: user=" + who_updated + ",player=" + username
                + ",status=" + str(is_updated) + ",method=" + update_user_data.__name__
            )
            return is_updated
    else:
        logging.critical(
            "Path is invalid or doesn't exist. Path should also contain destination file: path="
            + conf.PATH_TO_BLOCKED_USERS_FILE + ",method=" + update_user_data.__name__
        )
        return False


def prepare_line_to_write(who_prepared, username, description):
    description = sStr.safe_string(description, who_prepared).replace(",", " ").replace("  ", " ")
    username = sStr.safe_string(username, who_prepared)
    line_date = datetime.strptime(str(date.today()), "%Y-%m-%d").strftime('%d/%m/%Y')
    who_prepared = sStr.safe_string(who_prepared, who_prepared)
    return username + "," + description + "," + line_date + "," + who_prepared + "\n"
