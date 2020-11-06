import string
import random


class PasswordGenerator:
    def __init__(self):
        pass

    def generate_password(self, length, choices):
        if not choices:
            choices = string.ascii_letters

        all_choices = "".join(choices)
        result = []
        choice_index = 0
        while len(result) < length:
            if choice_index < len(choices):
                symbol = random.choice(choices[choice_index])
                result.append(symbol)
                choice_index += 1
                continue

            result.append(random.choice(all_choices))
        random.shuffle(result)

        return "".join(result)


