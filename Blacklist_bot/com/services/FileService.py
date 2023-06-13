from com import Main

USERS_LIST = []


def add_user_to_bl(username, description):
    USERS_LIST.append("{}-{}".format(username, description))


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
