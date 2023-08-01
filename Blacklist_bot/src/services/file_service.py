import os
import logging
from datetime import date
from datetime import datetime
import config as conf
from safe_str import SafeStr as sStr


def add_user_to_bl(who_added, username_to_bl, description):
    file = open(conf.PATH_TO_BLOCKED_USERS_FILE, mode="a", encoding="utf-8")
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
        with open(conf.PATH_TO_BLOCKED_USERS_FILE, "r", encoding="utf-8") as file:
            all_lines = file.readlines()
        with open(conf.PATH_TO_BLOCKED_USERS_FILE, "w", encoding="utf-8") as file:
            for line in all_lines:
                username_from_file = line.split(conf.SEPARATOR)[0]
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
        with open(conf.PATH_TO_BLOCKED_USERS_FILE, "r", encoding="utf-8") as file:
            all_lines = file.readlines()
        for line in all_lines:
            username_from_file = line.split(conf.SEPARATOR)[0]
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


def get_last_user_data():
    if os.path.exists(conf.PATH_TO_BLOCKED_USERS_FILE):
        with open(conf.PATH_TO_BLOCKED_USERS_FILE, 'rb') as file:
            try:  # catch OSError in case of a one line file
                file.seek(-2, os.SEEK_END)
                while file.read(1) != b'\n':
                    file.seek(-2, os.SEEK_CUR)
            except OSError:
                logging.warning("File: " + conf.PATH_TO_BLOCKED_USERS_FILE + " has only one line")
                file.seek(0)
            return file.readline().decode(encoding="utf-8")
    else:
        logging.critical(
            "Path is invalid or doesn't exist. Path should also contain destination file: path="
            + conf.PATH_TO_BLOCKED_USERS_FILE + ",method=" + get_user_data.__name__
        )
        return ""


def update_user_data(who_updated, username, description):
    is_updated = False
    if os.path.exists(conf.PATH_TO_BLOCKED_USERS_FILE):
        with open(conf.PATH_TO_BLOCKED_USERS_FILE, "r", encoding="utf-8") as file:
            all_lines = file.readlines()
        with open(conf.PATH_TO_BLOCKED_USERS_FILE, "w", encoding="utf-8") as file:
            for line in all_lines:
                username_from_file = line.split(conf.SEPARATOR)[0]
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
    description = sStr.safe_string(description, who_prepared)
    username = sStr.safe_string(username, who_prepared)
    line_date = datetime.strptime(str(date.today()), "%Y-%m-%d").strftime('%d/%m/%Y')
    who_prepared = sStr.safe_string(who_prepared, who_prepared)
    return username + conf.SEPARATOR + description + conf.SEPARATOR + line_date + conf.SEPARATOR + who_prepared + "\n"
