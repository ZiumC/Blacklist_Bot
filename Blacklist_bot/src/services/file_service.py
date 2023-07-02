import os
from datetime import date
from datetime import datetime
import src.config as conf
from src.safe_str import SafeStr as sStr


def add_user_to_bl(who_added, username_to_bl, description):
    file = open(conf.PATH_TO_BLOCKED_USERS_FILE, mode="a")
    if os.path.exists(conf.PATH_TO_BLOCKED_USERS_FILE):
        file.write(prepare_line_to_write(who_added, username_to_bl, description))
        file.close()
        return True
    else:
        return False


def remove_user_from_bl(username_to_remove):
    if os.path.exists(conf.PATH_TO_BLOCKED_USERS_FILE):
        with open(conf.PATH_TO_BLOCKED_USERS_FILE, "r") as file:
            all_lines = file.readlines()
        with open(conf.PATH_TO_BLOCKED_USERS_FILE, "w") as file:
            for line in all_lines:
                if not sStr.contains(line, username_to_remove):
                    file.write(line)
        return True
    else:
        return False


def get_user_data(username_to_check):
    if os.path.exists(conf.PATH_TO_BLOCKED_USERS_FILE):
        with open(conf.PATH_TO_BLOCKED_USERS_FILE, "r") as file:
            all_lines = file.readlines()
        for line in all_lines:
            if sStr.contains(line, username_to_check):
                return line
        return ""
    else:
        return ""


def update_user_data(who_updated, username, description):
    if os.path.exists(conf.PATH_TO_BLOCKED_USERS_FILE):
        with open(conf.PATH_TO_BLOCKED_USERS_FILE, "r") as file:
            all_lines = file.readlines()
        with open(conf.PATH_TO_BLOCKED_USERS_FILE, "w") as file:
            for line in all_lines:
                if sStr.contains(line, username):
                    file.write(prepare_line_to_write(who_updated, username, description))
                else:
                    file.write(line)
            return True
    else:
        return False


def prepare_line_to_write(who_prepared, username, description):
    description = sStr.safe_string(description).replace(",", " ").replace("  ", " ")
    username = sStr.safe_string(username)
    line_date = datetime.strptime(str(date.today()), "%Y-%m-%d").strftime('%d/%m/%Y')
    who_prepared = sStr.safe_string(who_prepared)
    return username + "," + description + "," + line_date + "," + who_prepared + "\n"
