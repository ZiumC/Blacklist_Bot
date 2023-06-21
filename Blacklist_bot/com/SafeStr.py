import re
BANNED_WORDS = ["https", "http", "/", "\\", ":", ".", "print", "{", "}"]
EMOJI_PATTERN = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)


class SafeStr:
    @staticmethod
    def safe_string(value):

        filtered = str(value)
        filtered = EMOJI_PATTERN.sub(r'', filtered)
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