import random
import string


def generate_string(length):
    characters = string.printable
    random_unicode_string = ''.join(random.choice(characters) for _ in range(length))
    return random_unicode_string
