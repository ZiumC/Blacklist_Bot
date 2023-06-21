BANNED_WORDS = ["https", "http", "/", "\\", ":", ".", "print", "{", "}"]


class SafeStr:
    @staticmethod
    def safe_string(value):

        filtered = str(value)
        for word in BANNED_WORDS:
            try:
                filtered.index(word)
            except ValueError:
                pass
            else:
                filtered = filtered.replace(word, " ")

        result = ""
        for i in range(0, len(filtered)):
            result += filtered[i]
        return result

    @staticmethod
    def contains(string, target):
        try:
            string.index(target)
        except ValueError:
            return False
        else:
            return True