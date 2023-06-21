from com.SafeStr import SafeStr as s
from com.Main import PATH_TO_BLOCKED_USERS_FILE as bl_path
from datetime import date
from datetime import datetime
import os

USERS_LIST = []


def add_user_to_bl(who_added, username_to_bl, description):

    file = open(bl_path, mode="a")

    if os.path.exists(bl_path):
        line_to_write = s.safe_string(username_to_bl) + "," + \
                        s.safe_string(description).replace(",", " ").replace("  ", " ") + "," \
                        + datetime.strptime(str(date.today()), "%Y-%m-%d").strftime('%d/%m/%Y') + ","\
                        + s.safe_string(who_added) + "\n"
        file.write(line_to_write)
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
