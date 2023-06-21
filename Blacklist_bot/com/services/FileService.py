from com.SafeStr import SafeStr as s
from com.Main import PATH_TO_BLOCKED_USERS_FILE as bl_path
from datetime import date
import os

USERS_LIST = []


def add_user_to_bl(username, description):

    file = open(bl_path, mode="a")

    if os.path.exists(bl_path):
        text_to_write = str(date.today()) + "," + s.safe_string(username) + "," + s.safe_string(description) + "\n"
        file.write(text_to_write)
        file.close()
        return True
    else:
        return False


def check_user(username):
    result = "Nothing found yet..."
    for line in USERS_LIST:
        if username in line:
            split_line = line.split("-")
            result = "User {} is on black list!\n" \
                     "Reason:\n" \
                     ":arrow_forward: {}"
            result.format(split_line[0], split_line[1])

    return result
