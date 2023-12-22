import string


class Check_password():

    def __init__(self):
        self.score = 0

    def check(self, password):
        upper_case = any([1 if i in string.ascii_uppercase else 0 for i in password])
        lower_case = any([1 if i in string.ascii_lowercase else 0 for i in password])
        special = any([1 if i in string.punctuation else 0 for i in password])
        digits = any([1 if i in string.digits else 0 for i in password])
        length = len(password)

        if length >= 8:
            length = True
        else:
            length = False

        characters = [upper_case, lower_case, special, digits, length]

        for i in range(len(characters)):
            if characters[i]:
                self.score += 1

        if self.score <= 1:
            color = 'red'
            verdict = 'ужасно'
        elif self.score == 2:
            color = 'red'
            verdict = 'плохо'
        elif self.score == 3:
            color = 'yellow'
            verdict = 'нормально'
        elif self.score == 4:
            color = 'green'
            verdict = 'хорошо'
        elif self.score == 5:
            color = 'green'
            verdict = 'отлично'
        return verdict, color
