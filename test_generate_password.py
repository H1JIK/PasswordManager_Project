import random
import string


class Generate:
    def __init__(self):
        self.number_of_digits = 4
        self.number_of_punctuation_characters = 2
        self.characters = string.ascii_letters + string.digits + string.punctuation
        self.password_length = 15
        self.password = ''

    def generate_password(self):
        for n_digits in range(self.number_of_digits):
            self.password += random.choice(string.digits)

        for n_punc in range(self.number_of_punctuation_characters):
            self.password += random.choice(string.punctuation)

        for n in range(self.password_length - self.number_of_digits - self.number_of_punctuation_characters):
            self.password += random.choice(string.ascii_letters)

        passw = list(self.password)
        random.shuffle(passw)
        self.password = ''.join(passw)

        return self.password
