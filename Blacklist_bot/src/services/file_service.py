from src.safe_str import SafeStr as s
from src.main import PATH_TO_BLOCKED_USERS_FILE as bl_path
from datetime import date
from datetime import datetime
import os


def add_user_to_bl(who_added, username_to_bl, description):
    file = open(bl_path, mode="a")
    if os.path.exists(bl_path):
        file.write(prepare_line_to_write(who_added, username_to_bl, description))
        file.close()
        return True
    else:
        return False


def remove_user_from_bl(username_to_remove):
    if os.path.exists(bl_path):
        with open(bl_path, "r") as file:
            all_lines = file.readlines()
        with open(bl_path, "w") as file:
            for line in all_lines:
                if not s.contains(line, username_to_remove):
                    file.write(line)
        return True
    else:
        return False


def get_user_data(username_to_check):
    if os.path.exists(bl_path):
        with open(bl_path, "r") as file:
            all_lines = file.readlines()
        for line in all_lines:
            if s.contains(line, username_to_check):
                return line
        return ""
    else:
        return ""


def update_user_data(who_updated, username, description):
    if os.path.exists(bl_path):
        with open(bl_path, "r") as file:
            all_lines = file.readlines()
        with open(bl_path, "w") as file:
            for line in all_lines:
                if s.contains(line, username):
                    file.write(prepare_line_to_write(who_updated, username, description))
                else:
                    file.write(line)
            return True
    else:
        return False


def prepare_line_to_write(who_prepared, username, description):
    description = s.safe_string(description).replace(",", " ").replace("  ", " ")
    username = s.safe_string(username)
    line_date = datetime.strptime(str(date.today()), "%Y-%m-%d").strftime('%d/%m/%Y')
    who_prepared = s.safe_string(who_prepared)
    return username + "," + description + "," + line_date + "," + who_prepared + "\n"
