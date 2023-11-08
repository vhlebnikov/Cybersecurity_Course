import random
import string
import unittest
import kuznechik


def generate_string(length, filename):
    characters = string.printable
    random_unicode_string = ''.join(random.choice(characters) for _ in range(length))

    f = open(filename, 'w')
    f.write(random_unicode_string)
    f.close()
    return random_unicode_string


master_key = int('8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef', 16)  # 32 bytes


class Tests(unittest.TestCase):
    def test_japanese(self):
        kuznechik.get_keys(master_key)
        x = kuznechik.get_string_from_file("files/input1.txt")
        x = kuznechik.text_to_bytes(x)
        actual_enc = kuznechik.encrypt(x)
        actual_dec = kuznechik.decrypt(actual_enc)
        actual_dec_text = kuznechik.bytes_to_text(actual_dec)

        print(actual_dec_text)
        print(x)
        print(actual_enc)
        print(actual_dec)

        f = open("files/input1.txt", "r")
        actual = f.read().encode('utf-8')
        f.close()
        self.assertEqual(actual, actual_dec_text)
        self.assertEqual(x, actual_dec)

