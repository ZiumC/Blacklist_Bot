from com.SafeStr import SafeStr as s
from com.Main import PATH_TO_BLOCKED_USERS_FILE as bl_path
from datetime import date
from datetime import datetime
import os


def add_user_to_bl(who_added, username_to_bl, description):
    file = open(bl_path, mode="a")
    if os.path.exists(bl_path):
        line_to_write = s.safe_string(username_to_bl) + "," + \
                        s.safe_string(description).replace(",", " ").replace("  ", " ") + "," \
                        + datetime.strptime(str(date.today()), "%Y-%m-%d").strftime('%d/%m/%Y') + "," \
                        + s.safe_string(who_added) + "\n"
        file.write(line_to_write)
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
                if not s.contains(line.strip("\n"), username_to_remove):
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