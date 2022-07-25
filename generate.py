import secrets
import string


class Generator:
    def __init__(self):
        # Changeable via Settings-Page
        self.setting_upper = True
        self.setting_lower = True
        self.setting_digits = True
        self.setting_punctuation = True
        self.setting_length = 15

    def generate_pw(self):
        char_set = ""

        if self.setting_upper:
            char_set += string.ascii_uppercase
        if self.setting_lower:
            char_set += string.ascii_lowercase
        if self.setting_digits:
            char_set += string.digits
        if self.setting_punctuation:
            char_set += string.punctuation

        return "".join([secrets.choice(char_set) for i in range(self.setting_length)])
